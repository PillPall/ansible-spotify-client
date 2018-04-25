# Spotify search

#### Modules
spotify_update_playlists - Ansible module to update user playlists

* Synopsis
* Options
* Examples
* Return value

#### Synopsis

Ansible module to add or remove tracks to/from a user playlist. Tracks and playlists can be provided via **URI or JSON File**. A JSON file can be generated using the Ansible module `spotify_search`, `spotify_user_playlists` or `spotify_artists_top_tracks` or visit this site for more informations [Link Playlists](https://beta.developer.spotify.com/documentation/web-api/reference/playlists/create-playlist/) [Link Tracks](https://beta.developer.spotify.com/documentation/web-api/reference/tracks/get-several-tracks/).

You can only define one of the `playlist_id` and `playlist-file` options.

You can only define one of the `track_file` and `track_file` options.

You can combine these options for **playlist** and **track**.

The option `dest_file` can be combined with all states.

#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------  |----------- |--------- | -------- |
| auth_token  | String        | Yes        | null       | null     | Spotify authentication token generated from the module `spotify_auth` and `spotify_auth_create_user_token` |
| state         | String      | Yes        | null | add, remove | Add or remove tracks from playlist |
| username      | String      | Yes        | null       | null     | Spotify Username |
| playlist_file | String      | No         | null       | null     | JSON File containing a dict of Playlist ID or URI to update. |
| playlist_id   | String       | No        | null       | null     |  Playlist ID or URI to update. |
| track_id      | String       | No        | null       | null     |  Track ID or URI to update. |
| track_file    | String       | No        | null       | null     |  JSON File containing a dict of Track IDs or URIs to update. |
| dest_file     | String       | No        | null       | null     |  Destination file to save the output to. |


#### Requirements  
* python >= 2.7.10
* spotipy >= 2.4.4

#### Examples
```
- name: Add songs to playlist from playlist_file with defined track uri
  spotify_update_playlists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    username: "USER"
    state: "add"
    playlist_file: "{{ playbook_dir }}/files/create_playlist_user.json"
    track_id: spotify:track:1YZDkJOFT8xlAXDi8lneb3

- name: Add songs to playlist with playlist_id with defined track_file and dest_file
  spotify_update_playlists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    username: "USER"
    state: "add"
    playlist_id: spotify:user:USER:playlist:BCASDJLASDKV12345
    track_file: "{{ playbook_dir }}/files/tracks.json"
    dest_file: "{{ dest_file }}"

- name: Remove songs from playlist with playlist_file and defined track_file
  spotify_update_playlists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    username: "USER"
    state: "remove"
    playlist_file: "{{ playbook_dir }}/files/create_playlist_user.json"
    track_file: "{{ playbook_dir }}/files/tracks.json"

- name: Remove songs from playlist with playlist_id and defined track_id
  spotify_update_playlists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    username: "USER"
    state: "remove"
    playlist_id: spotify:user:USER:playlist:BCASDJLASDKV12345
    track_id: spotify:track:1YZDkJOFT8xlAXDi8lneb3
    dest_file: "{{ playbook_dir }}/files/update_playlist_user.json"

#
# Example of how to use spotify_artists_top_tracks module to update a playlist
#
- name: Get top tracks for artist Young the Giant
  spotify_artists_top_tracks:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_name: "Young the Giant"
    dest_file: "{{ playbook_dir }}/files/tracks.json"

- name: Add Young the giant top tracks to a playlist
  spotify_update_playlists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    username: "USER"
    state: "add"
    playlist_id: spotify:user:USER:playlist:BCASDJLASDKV12345
    track_file: "{{ playbook_dir }}/files/tracks.json"
```

#### RETURN VALUES:
```
output:
  description: "returns a dict with the snapshot_ids of the updated playlists"
  returned: on success
  sample:
    changed: True
    result:
        snapshot_id: 4HJAHdr2BypGxe/esgasdfihIMcv4luhnZlAhGXL295BefUSisFtRjl0D8CxGqaVrY
  type: dict
```
