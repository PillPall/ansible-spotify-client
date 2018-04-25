# Spotify player

#### Modules
spotify_player - Ansible module for controlling your spotify

* Synopsis
* Options
* Examples
* Return value

#### Synopsis

Ansible module for controlling your spotify. Play or pause a song, toggle repeat or shuffle, set volume, set transfer playback to a different device.

#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------|----------- |--------- | -------- |
| auth_token  | String       | True     | null       | null     | Spotify authentication token generated from the module `spotify_auth` and `spotify_auth_create_user_token` |
| state         | String      | True       | null       | play, pause, next, previous, repeat, shuffle, transfer_playback, volume     | Action to trigger. |
| device_id     | String      | False       | null       |        | Device ID you want to transfer the playback to. |
| repeat_mode   | String      | False       | null       | track, context, off | Set repeat mode. |
| toggle_shuffle | String      | False       | null       | on, off | Set shuffle mode. |
| volume_level | Integer      | False       | null       | null | Volume level in percent. |


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
