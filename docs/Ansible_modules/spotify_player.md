# Spotify player

#### Modules
spotify_player - Ansible module for controlling your spotify

* Synopsis
* Options
* Examples
* Return value

#### Synopsis

Ansible module for controlling your spotify. Play or pause a song, toggle repeat or shuffle, set volume, set transfer playback to a different device.

To **play a specific song** define the option `track_uri` or `track_file`. `track_file` accept files created by the Ansible modules `spotify_artists_top_tracks`, `spotify_user_info` or `spotify_search`.

To **play songs from a specific artist** define the option `artist_uri` or `artist_file`. `artist_file` accept files created by the Ansible modules `spotify_related_artists`, `spotify_user_info` or `spotify_search`.

To **play a specific playlist** define the option `playlist_uri` or `playlist_file`. `playlist_file` accept files created by the Ansible modules `spotify_user_playlists` or `spotify_search`.

To **play a specific album** define the option `album_uri` or `album_file`. `album_file` accept files created by the Ansible modules `spotify_search`.

#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------|----------- |--------- | -------- |
| auth_token  | String       | Yes     | null       | null     | Spotify authentication token generated from the module `spotify_auth` and `spotify_auth_create_user_token` |
| state         | String      | Yes       | null       | play, pause, next, previous, repeat, shuffle, transfer_playback, volume     | Action to trigger. |
| device_id     | String      | No       | null       |        | Device ID you want to transfer the playback to. |
| repeat_mode   | String      | No       | null       | track, context, off | Set repeat mode. |
| toggle_shuffle | String      | No       | null       | on, off | Set shuffle mode. |
| volume_level | Integer      | No       | null       | null | Volume level in percent. |
| album_uri | String      | No       | null       | null | Define album to play tracks from|
| album_file | String      | No       | null       | null | Define album file to play tracks from|
| artist_uri | String      | No       | null       | null | Define artist to play tracks from|
| artist_file | String      | No       | null       | null | Define artist file to play tracks from|
| track_uri | String      | No       | null       | null | Define track to play|
| track_file | String      | No       | null       | null | Define track file to play|
| playlist_uri | String      | No       | null       | null | Define a playlist to play|
| playlist_file | String      | No       | null       | null | Define a playlist file to play|

#### Requirements  
* python >= 2.7.10
* spotipy >= 2.4.4

#### Examples
```
- name: Play track
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: play

- name: Play next track
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: next

- name: Play previous track
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: next

- name: Set repeat to repeat a single track
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    repeat_mode: track
    state: repeat

- name: Turn on shuffle
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    toggle_shuffle: on
    state: shuffle

- name: Transfer playback to a new device
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    device_id: 0123456789ABCDEFGHI
    state: transfer_playback

- name: Set playback volume on device to 80%
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    volume_level: 80
    state: volume

- name: Play tracks from an album via given album_uri
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: play
    album_uri: spotify:album:4HDqXJvheEra3d0FtRBNvM

- name: Play tracks from an album via given album_uri
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: play
    album_file: "{{ playbook_dir }}/../files/search_result_artists_integration_test.json"

- name: Play tracks from an artist via given artist_uri
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: play
    artist_uri: spotify:artist:7oaSITFPadI3fnIxbv7hTa

- name: Play tracks from an artist via given artist_file
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: play
    artist_file: "{{ playbook_dir}}/../files/search_result_artists_integration_test_short.json"

- name: Play tracks from a playlist via given playlist_uri
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: play
    playlist_uri: spotify:user:1176221055:playlist:16YxsO6KwbhNOdJ25pUkeg

- name: Play tracks from an album via given album_uri
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: play
    playlist_file: "{{ playbook_dir }}/../files/search_result_playlists_integration_test.json"

- name: Play tracks via given track_uri
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: play
    track_uri: spotify:track:1ZJfXmUfrfP2p6v9TzWWiL

- name: Play tracks from an album via given album_uri
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: play
    track_file: "{{ playbook_dir }}/../files/search_result_tracks.json"
```    

#### RETURN VALUES:
```
output:
  description: "Returns null."
  returned: on success
  sample:
    changed: True
    result: null
  type: null
```
