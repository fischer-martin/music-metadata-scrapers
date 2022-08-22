#!/usr/bin/env python3

import os
import spotipy
import json
import alive_progress
import argparse



def read_file_content(filename, is_json = False):
    with open(filename, "r") as file:
        if is_json:
            file_content = json.load(file)
        else:
            file_content = file.read()

    return file_content

def fetch_releases(release_id_list):
    return spotify.albums(release_id_list)

def strip_artist(artist):
    possible_keys = ["external_urls", "followers", "href", "images", "popularity", "uri"]
    for key in possible_keys:
        artist.pop(key, None)

def strip_track(track):
    for artist in track["artists"]:
        strip_artist(artist)
    track.pop("available_markets")
    track.pop("external_urls")
    track.pop("href")
    track.pop("is_local")
    track.pop("preview_url")
    track.pop("uri")

def strip_album(album):
    # see https://developer.spotify.com/documentation/web-api/reference/#/operations/get-multiple-albums
    if "artists" in album:
        for artist in album["artists"]:
            strip_artist(artist)
    album.pop("available_markets")
    album.pop("external_urls")
    album.pop("href")
    album.pop("images")
    album.pop("popularity")
    album.pop("uri")
    album["tracks"].pop("href")
    album["tracks"].pop("limit")
    album["tracks"].pop("next")
    album["tracks"].pop("offset")
    album["tracks"].pop("previous")
    album["tracks"].pop("total")
    for track in album["tracks"]["items"]:
        strip_track(track)

def write_entries(albums, file, pretty_print = True, strip_unnecessary = False):
    for album in albums["albums"]:
        tracks = album["tracks"]
        while tracks["next"]:
            tracks = spotify.next(tracks)
            album["tracks"]["items"] = album["tracks"]["items"] + tracks["items"]

        if strip_unnecessary:
            strip_album(album)

        json.dump(album, file, indent = (4 if pretty_print else None), ensure_ascii = False)
        file.write("\n")

def count_release_ids(releases):
    i = 0
    for release in releases.values():
        i = i + len(release["spotify"])
    return i


argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input-file", help = "file containing album IDs", type = str, required = True)
argparser.add_argument("-c", "--credentials", help = "spotify API client id and client secret", nargs = 2)
argparser.add_argument("-o", "--output", help = "output file for storing albums", type = str, required = True)
argparser.add_argument("-p", "--pretty-print", help = "pretty print output", action = "store_true")
#argparser.add_argument("-r", "--remove-unnecessary", help = "remove unnecessary data from output", action = "store_true") # TODO: check the API doc if there are more fields that should be removed
args = argparser.parse_args()

releases = read_file_content(args.input_file, True)

spotipy_client_id_env_var_name = "SPOTIPY_CLIENT_ID"
spotipy_client_secret_env_var_name = "SPOTIPY_CLIENT_SECRET"

if args.credentials:
    os.environ[spotipy_client_id_env_var_name] = args.credentials[0]
    os.environ[spotipy_client_secret_env_var_name] = args.credentials[1]
elif spotipy_client_id_env_var_name not in os.environ or spotipy_client_secret_env_var_name not in os.environ:
    argparser.error("credentials not specified")

spotify = spotipy.Spotify(auth_manager = spotipy.oauth2.SpotifyClientCredentials())

# This syntax for context managers was officially introduced in 3.10 but also
# seems to work in 3.9 (at least for CPython). Could be rewritten as e.g. a nested
# with but I'm on Arch so why shouldn't I use bLeEdInG eDgE software?
# https://stackoverflow.com/a/31039332
with (open(args.output, "w") as output_file,
        alive_progress.alive_bar(count_release_ids(releases)) as bar):
    release_id_list = []
    i = 0
    for release in releases.values():
        for release_id in release["spotify"]:
            i = i + 1
            release_id_list.append(release_id)
            if i == 20:
                write_entries(fetch_releases(release_id_list), output_file, args.pretty_print, args.remove_unnecessary)
                bar(20) # pylint: disable=not-callable
                release_id_list = []
                i = 0

    if release_id_list:
        write_entries(fetch_releases(release_id_list), output_file, args.pretty_print, args.remove_unnecessary)
        bar(i) # pylint: disable=not-callable
