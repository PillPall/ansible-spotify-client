# Spotify search

#### Modules
spotify_search - Ansible module to query searches in Spotify

* Synopsis
* Options
* Examples
* Return value

#### Synopsis

Ansible module to search in Spotify for Artists, Tracks, Albums, Artists & Track, Artists & Album or public Playlists via the Spotify API.

Except for the states **artists_and_albums** and **artists_and_tracks** you can only define one of the options `albums_name`, `artists_name`, `playlists_name` or `tracks_name`.

To search for `artists_and_albums` you need to define `albums_name` and `artists_name`.

To Search for `artists_and_tracks` you need to define `albums_name` and `tracks_name`.

The playlist search only allows you to search through public playlists. If you want to search through your personal playlists use the module `spotify_user_playlists`.

The options `dest_file`, `limit` and `output_format` can be combined with all states.

Informations about the output format can be found here [link](https://developer.spotify.com/web-api/search-item/).

#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------|----------- |--------- | -------- |
| auth_token  | String       | True     | null       | null     | Spotify authentication token generated from the module `spotify_auth` and `spotify_auth_create_user_token` |
| state | String | True | null | artists, tracks, playlists, albums, artists_and_albums, artists_and_tracks | Search to trigger. |
| albums_name | String | False | null | null | Name of an album. |
| artists_name | String | False | null | null | Name of an artist. |
| playlists_name | String | False | null | null | Name of an public playlist. |
| tracks_name | String | False | null | null | Name of an track. |
| limit | String | False | null | null | Limit the search output. |
| dest_file     | String       | No     | null       | null     |  Destination file to save the output to. |
| output_format  | String      | No     | long       | short, long |  Control Ansible output format. |

#### Requirements  
* python >= 2.7.10
* spotipy >= 2.4.4

#### Examples
```
- name: Search for artist Young the Giant and return maximum 10 search results
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: long
    state: artists
    artists_name: Young the Giant
    limit: 10
  register: artists_search_result

- name: Search for track containing Coug*
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    state: tracks
    tracks_name: Coug*

- name: Search for playlist Colombia with wildcard at the end and return maximum 20 search results
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: long
    state: playlists
    playlists_name: Colombia*
    limit: 20

- name: Search for Albums Arrival and return maximum 20 search results and save the output to a file
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    dest_file: search_result_albums.json
    output_format: long
    state: album
    albums_name: Arrival
    limit: 20

- name: Search for artists and album in combination
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: short
    state: artists_and_albums
    albums_name: Coexist
    artists_name: The xx
    limit: 20

- name: Search for artists and tracks in combination
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: short
    state: artists_and_albums
    tracks_name: Fiction
    artists_name: The xx
    limit: 20
```

#### RETURN VALUES:
```
output:
  description: "returns a dict with the search result for artists and album in output_format short."
  returned: on success
  sample:
    changed: True
    result:
        albums:
        - album: Coexist
          artist: The xx
          uri: spotify:album:2cRMVS71c49Pf5SnIlJX3U
  type: dict

output:
  description: "returns a dict with the search result for playlists in output_format long."
  returned: on success
  sample:
    changed: True
    result:
        playlists:
          items:
          - name: Éxitos Colombia
            collaborative: false
            external_urls:
              spotify: https://open.spotify.com/user/spotify/playlist/37i9dQZF1DXbvPjXfc8G9S
            uri: spotify:user:spotify:playlist:37i9dQZF1DXbvPjXfc8G9S
            public:
            owner:
              display_name: Spotify
              external_urls:
                spotify: https://open.spotify.com/user/spotify
              uri: spotify:user:spotify
              href: https://api.spotify.com/v1/users/spotify
              type: user
              id: spotify
            tracks:
              total: 50
              href: https://api.spotify.com/v1/users/spotify/playlists/37i9dQZF1DXbvPjXfc8G9S/tracks
            href: https://api.spotify.com/v1/users/spotify/playlists/37i9dQZF1DXbvPjXfc8G9S
            snapshot_id: yBnt8hL8bFyoPN+8/MHVPC2CkSi5haDTCspx9821mGoNpNavK/gqauQlyoyl868VnUTf4ruylv0=
            images:
            - url: https://i.scdn.co/image/36d98030a7d4651025b385433a839d260e399b9f
              width: 300
              height: 300
            type: playlist
            id: 37i9dQZF1DXbvPjXfc8G9S
  type: dict

output:
  description: "returns a dict with the search result for an artists."
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


output:
  description: "returns a dict with the search result for artists and tracks in output_format short."
  returned: on success
  sample:
    changed: True
    result:
        tracks:
        - track: Cough Syrup
          uri: spotify:track:1UqhkbzB1kuFwt2iy4h29Q
          artist: Young the Giant
        - track: Cough Syrup
          uri: spotify:track:4Tfe8Uu9faFdWRiZbpvpXd
          artist: Young the Giant
  type: dict
  ```
