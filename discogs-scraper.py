#!/usr/bin/env python3

import os
import discogs_client
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

def fetch_release(release_id):
    release = discogs.release(release_id)

    # We also fetch the release's tracklist so that we actually get the entire data since
    # discogs.release() doesn't actually seem to fetch anything until we access one of
    # its members like tracklist or title (but not data which is what we actually need).
    release.tracklist

    return release.data

def strip_release(release):
    # TODO
    pass

def write_entry(entry, file, pretty_print = False, strip_unnecessary = False):
    if strip_unnecessary:
        strip_release(entry)

    json.dump(entry, file, indent = (4 if pretty_print else None), ensure_ascii = False)
    file.write("\n")

def count_release_ids(releases):
    i = 0
    for release in releases.values():
        i = i + len(release["discogs"])
    return i


argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input-file", help = "file containing album IDs", type = str, required = True)
argparser.add_argument("-t", "--token", help = "discogs API user token", required = True)
argparser.add_argument("-o", "--output", help = "output file for storing albums", type = str, required = True)
argparser.add_argument("-a", "--user-agent", help = "user-agent for API requests", type = str, default = "discogs-scraper/1.0")
argparser.add_argument("-p", "--pretty-print", help = "pretty print output", action = "store_true")
#argparser.add_argument("-r", "--remove-unnecessary", help = "remove unnecessary data from output", action = "store_true") # TODO: check the API doc for fields that should be removed
args = argparser.parse_args()

releases = read_file_content(args.input_file, True)

discogs = discogs_client.Client(args.user_agent, user_token = args.token)

# This syntax for context managers was officially introduced in 3.10 but also
# seems to work in 3.9 (at least for CPython). Could be rewritten as e.g. a nested
# with but I'm on Arch so why shouldn't I use bLeEdInG eDgE software?
# https://stackoverflow.com/a/31039332
with (open(args.output, "w") as output_file,
        alive_progress.alive_bar(count_release_ids(releases)) as bar):
    for release in releases.values():
        for release_id in release["discogs"]:
            write_entry(fetch_release(release_id), output_file, args.pretty_print)
            bar() # pylint: disable=not-callable
