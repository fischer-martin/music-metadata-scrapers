### Usage
#### `spotify-scraper.py`
```
usage: spotify-scraper.py [-h] -i INPUT_FILE [-c CREDENTIALS CREDENTIALS] -o OUTPUT [-p]

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        file containing album IDs
  -c CREDENTIALS CREDENTIALS, --credentials CREDENTIALS CREDENTIALS
                        spotify API client id and client secret
  -o OUTPUT, --output OUTPUT
                        output file for storing albums
  -p, --pretty-print    pretty print output
```
See [Spotipy API documentation](https://spotipy.readthedocs.io/en/master/#getting-started) for information about the client ID/secret.

#### `discogs-scraper.py`
```
usage: discogs-scraper.py [-h] -i INPUT_FILE -t TOKEN -o OUTPUT [-a USER_AGENT] [-p]

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        file containing album IDs
  -t TOKEN, --token TOKEN
                        discogs API user token
  -o OUTPUT, --output OUTPUT
                        output file for storing albums
  -a USER_AGENT, --user-agent USER_AGENT
                        user-agent for API requests
  -p, --pretty-print    pretty print output
```
See [Discogs API client documentation](https://python3-discogs-client.readthedocs.io/en/latest/authentication.html#user-token-authentication) for information on how to get a user token.

#### JSON Input Format
```
{
    "<album identifier>": {
        "spotify": [
            <spotify album identifiers>
        ],
        "discogs": [
            <discogs release identifiers>
        ]
    },
    ...
}
```
**Spotify album IDs** are taken from the URL: `https://open.spotify.com/album/5Z9iiGl2FcIfa3BMiv6OIw` would give us the ID `5Z9iiGl2FcIfa3BMiv6OIw`.  
**Discogs release IDs** are also taken from the URL: `https://www.discogs.com/release/179372-Rick-Astley-Whenever-You-Need-Somebody` would give us the ID `179372`. Watch out for the `release` in the URL. It is easy to confuse it with a `master` (which is basically a collection releases, e.g. the CD and the vinyl release of the same album).

The only important thing is that there is a global JSON object that contains objects that have arrays with keys `spotify` and `discogs`.  
If there is no need for keeping an organized JSON release file, one could of course only provide one object within the global object and throw every release ID into the corresponding array. The output is in no way associated with the input (except of course in the way that it contains the releases for the IDs provided).

### Dependencies
* Python 3.10
    * **should** also work with CPython 3.9 but I can't guarantee that (support for the corresponding language features has only been added unofficially in version 3.9)
    * should also work for lower versions if the context managers in [discogs-scraper.py](discogs-scraper.py) and [spotify-scraper.py](spotify-scraper.py) are rewritten to not use the [3.10 syntax](https://stackoverflow.com/a/31039332)
* [python3-discogs-client](https://pypi.org/project/python3-discogs-client/) (works with version 2.3.15)
* [spotipy](https://pypi.org/project/spotipy/) (works with version 2.20.0)
* [alive-progress](https://pypi.org/project/alive-progress/) (works with version 2.4.1)
