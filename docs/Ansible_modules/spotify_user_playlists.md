# Spotify user informations

#### Modules
spotify_user_playlists - Ansible module to get all users playlists, create a playlist or search for a playlist.

* Synopsis
* Options
* Examples
* Return value

#### Synopsis

Ansible module to get all users playlists, create a playlist or search for a playlist.

The options `playlist_description`, `public` and `username` are only necessary for creating a playlist. The parameter `username` has to be the same like the one used for authentication.

`playlist_name` has to be defined for `search` and `create` a playlist.

`limit` is only a valid option for `search` and `get_all`.

The options `dest_file` and `output_format` can be combined with all states.

#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------  |--------- |--------- | -------- |
| auth_token    | String      | Yes        | null     | null     | Spotify authentication token generated from
| state         | String      | Yes        | null     | get_all, create, search | Action to trigger. |
| dest_file     | String      | No         | null     | null     |  Destination file to save the output to. |
| output_format | String      | No         | long     | short, long |  Control Ansible output format. |
| limit         | integer     | No         | 50       | null     | Limit the amount of the user playlists to get or to search for. |
| playlist_description   | String      | No         | null     | null     |  Playlist description for creating a new playlist |
| playlist_name | String      | No         | null     | null     |  Name of the playlist to search for or to create. |
| public   | String      | No         | no     | yes, no     | Create a playlist as public or non-public playlist |
| username      | String      | No        | null     | null     | Spotify Username for creating a playlist|

#### Requirements  
* python >= 2.7.10
* spotipy >= 2.4.4

#### Examples
```
- name: Get the first 20 user playlists for user muster and save the output to dest_file
  spotify_get_user_playlist:
    auth_token: 0123456789ABCDEFGHI
    dest_file: artists.json
    state: get_all
    limit: 20

- name: Get the first 100 user playlists for user muster and save the output to dest_file
  spotify_get_user_playlist:
    auth_token: 0123456789ABCDEFGHI
    dest_file: artists.json
    state: get_all
    limit: 100

- name: Create a non-pbulic playlist with defined playlist_description
  spotify_get_user_playlist:
    auth_token: 0123456789ABCDEFGHI
    playlist_description: Playlist created with Ansible
    playlist_name: Ansible_Playlist
    public: no
    state: create

- name: Create a pbulic playlist with defined playlist_description
  spotify_get_user_playlist:
    auth_token: 0123456789ABCDEFGHI
    playlist_description: Public playlist created with Ansible
    playlist_name: Ansible_public_Playlist
    public: yes
    state: create

- name: Search in the first 20 User playlists for a Playlist named Ansible_Playlist
  spotify_get_user_playlist:
    auth_token: 0123456789ABCDEFGHI
    limit: 20
    playlist_name: Ansible_Playlist
    state: search
```
#### RETURN VALUES:
```
---
output:
  description: "returns a dict with informations about a created playlist"
  returned: on success with state create and output_format long
  sample:
    changed: True
    result:
        href: https://api.spotify.com/v1/users/USER/playlists?offset=0&limit=50
        items:
        - collaborative: false
          external_urls:
            spotify: https://open.spotify.com/user/USER/playlist/ABCDEFGHIJKL
          href: https://api.spotify.com/v1/users/USER/playlists/ABCDEFGHIJKL
          id: ABCDEFGHIJKL
          images: []
          name: Ansible 3
          owner:
            display_name:
            external_urls:
              spotify: https://open.spotify.com/user/USER
            href: https://api.spotify.com/v1/users/USER
            id: USER
            type: user
            uri: spotify:user:USER
          primary_color:
          public: false
          snapshot_id: ABCDEFGHIJKL1234567890
          tracks:
            href: https://api.spotify.com/v1/users/USER/playlists/ABCDEFGHIJKL/tracks
            total: 0
          type: playlist
          uri: spotify:user:USER:playlist:ABCDEFGHIJKL
  type: dict

output:
  description: "returns a dict with informations about a"
  returned: on success for state get_all with output_format short
  sample:
    changed: True
    result:
        playlists:
        - name: Ansible non public playlist
          uri: spotify:user:USER-m:playlist:ABCDEFGHIJKL
        - name: Ansible public playlist
          uri: spotify:user:USER-m:playlist:ABCDEFGHIJKL
  type: dict
```
