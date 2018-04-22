> SPOTIFY_SEARCH    (./ansible/library/spotify_search.py)

        Ansible module to search in Spotify for Artists, Tracks, Albums, Artists & Track, Artists & Album or public Playlists via the Spotify API.

OPTIONS (= is mandatory):

- albums_name
        Album name to search for.
        [Default: (null)]
        type: String

- artists_name
        Artists name to search for.
        [Default: (null)]
        type: String

= auth_token
        Spotify API authentication token

        type: String

- dest_file
        Path to file to save the search result.
        [Default: (null)]
        type: String

- limit
        Limit the playlist get_all to
        [Default: 10]
        type: Integer

- output_format
        Control Ansible output.
        (Choices: short, long)[Default: long]
        type: String

- playlists_name
        Playlist name to search for.
        [Default: (null)]
        type: String

= state
        Parameter to define what to search for.
        (Choices: artists, tracks, playlists, albums, artists_and_albums, artists_and_tracks)
        type: String

- tracks_name
        Track name to search for.
        [Default: (null)]
        type: String


REQUIREMENTS:  python >= 2.7.10, spotipy >= 2.4.4

AUTHOR: Michael Bloch (github@mbloch.de)
        METADATA:
          status:
          - preview
          supported_by: community


EXAMPLES:
- name: Search for artist Young the Giant and return maximum 10 search results
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: long
    state: artists
    artists_name: Young the Giant
    limit: 10
  register: artists_search_result

- name: Search for artists start with Young maximum 50 search results
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: long
    state: artists
    artists_name: Young
    limit: 50
  register: artists_search_result

- name: Search for track cough syrup, return maximum 20 search results and save it to search_result_tracks.json
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    dest_file: search_result_tracks.json
    output_format: short
    state: tracks
    tracks_name: cough syrup
    limit: 20

- name: Search for track containing Coug*, return maximum 20 search results and save it to search_result_tracks.json
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    dest_file: search_result_tracks.json
    output_format: short
    state: tracks
    tracks_name: Coug*
    limit: 20

- name: Search for playlist Colombia with wildcard at the end and return maximum 20 search results
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: long
    state: playlists
    playlists_name: Colombia*
    limit: 20

- name: Search for Albums Arrival and return maximum 20 search results
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    dest_file: search_result_albums.json
    output_format: long
    state: tracks
    albums_name: Arrival
    limit: 20

- name: Search for Artists starts with Ab* and all Albums Start with Arr and return maximum 20 search results
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    dest_file: search_result_albums.json
    output_format: long
    state: tracks
    artists_name: Ab*
    albums_name: Arr*
    limit: 20

RETURN VALUES:


---
output:
  description: "returns a dict with the search result.
  More information about the search result output can be found here https://developer.spotify.com/web-api/search-item/"
  returned: on success
  sample:
    changed: True
    result:
        artists:
          href: https://api.spotify.com/v1/search?query=artist%3AYoung+the+Giant&type=artist&offset=0&limit=1
          items:
          - external_urls:
              spotify: https://open.spotify.com/artist/4j56EQDQu5XnL7R3E9iFJT
            followers:
              href:
              total: 780072
            genres:
            - indie pop
            - indie rock
            - indietronica
            - la indie
            - modern rock
            - shimmer pop
            - stomp and holler
            href: https://api.spotify.com/v1/artists/4j56EQDQu5XnL7R3E9iFJT
            id: 4j56EQDQu5XnL7R3E9iFJT
            images:
            - height: 640
              url: https://i.scdn.co/image/04ec224d5a225ef58b300d9942af24b7e2ad3320
              width: 640
            - height: 320
              url: https://i.scdn.co/image/f4dbc17572a1b8010ffdea9b6d43acec2d92b004
              width: 320
            - height: 160
              url: https://i.scdn.co/image/5eb442e4c439d9e7799a1a26fe67fad075ad80fa
              width: 160
            name: Young the Giant
            popularity: 68
            type: artist
            uri: spotify:artist:4j56EQDQu5XnL7R3E9iFJT
          limit: 1
          next:
          offset: 0
          previous:
          total: 1
  type: dict
