# Spotify user informations

#### Modules
spotify_user_info - Ansible module to get informations about the current User.

* Synopsis
* Options
* Examples
* Return value

#### Synopsis

Ansible module to get different informations about the current user. Following information can you get with this module:
* current playback
* Devices
* Recently played tracks
* Top Tracks
* Top Artists
* User informations

The options `limit` and ``time_range`` can only defined together with the state `recently_played`, `top_tracks` and `top_artists`.

The options `dest_file` and `output_format` can be combined with all states.

#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------  |--------- |--------- | -------- |
| auth_token    | String      | Yes        | null     | null     | Spotify authentication token generated from
| state         | String      | Yes       | null     | current_playback, devices, recently_played, top_tracks, top_artists, user_info | User info to get. |
| dest_file     | String      | No         | null     | null     |  Destination file to save the output to. |
| limit         | integer     | No         | 50       | null     | Limit the output for top artists, top tracks or recently played tracks. |
| output_format | String      | No         | long     | short, long |  Control Ansible output format. |
| time_range    | String      | No         | medium_term     | short_term, medium_term, long_term |  Time range for seeing users top artists and top tracks. |

#### Requirements  
* python >= 2.7.10
* spotipy >= 2.4.4

#### Examples
```
- name: Get infos about users current playback and save it to a file
  spotify_user_info:
    auth_token: 0123456789ABCDEFGHI
    dest_file: "{{ playbook_dir }}/files/current_user_playback.json"
    state: current_playback

- name: Get all available devices for a user
  spotify_user_info:
    auth_token: 0123456789ABCDEFGHI
    output_format: short
    state: devices

- name: Get users top 50 recently played tracks
  spotify_user_info:
    auth_token: 0123456789ABCDEFGHI
    dest_file: "{{ playbook_dir }}/files/users_recently_played_tracks.json"
    limit: 50
    output_format: short
    state: recently_played

- name: Get users top 40 played tracks
  spotify_user_info:
    auth_token: 0123456789ABCDEFGHI
    dest_file: "{{ playbook_dir }}/files/users_top_tracks.json"
    limit: 40
    output_format: short
    state: top_tracks

- name: Get users top 40 played artists
  spotify_user_info:
    auth_token: 0123456789ABCDEFGHI
    dest_file: "{{ playbook_dir }}/files/users_top_tracks.json"
    limit: 40
    output_format: short
    state: top_artists

- name: Get information about the current user
  spotify_user_info:
    auth_token: 0123456789ABCDEFGHI
    output_format: short
    state: user_info
```
#### RETURN VALUES:
```
output:
  description: "returns a dict with the result for state top_artists"
  returned: on success for state top_artists
  sample:
    changed: True
    result:
        items:
        - genres:
          - folk-pop
          - indie folk
          - neo mellow
          - south african pop
          name: Mumford & Sons
          external_urls:
            spotify: https://open.spotify.com/artist/3gd8FJtBJtkRxdfbTu19U2
          popularity: 78
          uri: spotify:artist:3gd8FJtBJtkRxdfbTu19U2
          href: https://api.spotify.com/v1/artists/3gd8FJtBJtkRxdfbTu19U2
          followers:
            total: 4160683
            href:
          images:
          - url: https://i.scdn.co/image/8dff0f92819275feabea7fb4c65d1409a1a99127
            width: 1000
            height: 1000
          - url: https://i.scdn.co/image/d6104bcaabe6854be406e5743d9bde6716e7d0fe
            width: 640
            height: 640
          - url: https://i.scdn.co/image/ed2faba8c2ec01a4d8418905fa3f96f3b8e7cc9d
            width: 200
            height: 200
          - url: https://i.scdn.co/image/b6628e4a0d426b3d1d93bbe49fc5ab9a2a9a9301
            width: 64
            height: 64
          type: artist
          id: 3gd8FJtBJtkRxdfbTu19U2
  type: dict

output:
  description: "returns a dict with the result for state recently_played with defined output_format short"
  returned: on success for state recently_played
  sample:
    changed: True
    result:
      tracks:
       album: Riot On An Empty Street
        artists: Kings of Convenience
        track: Know-How
        uri: spotify:track:4xqowxjJ03RWog4teL6oqG

output:
  description: "returns a dict with the result for state devices with defined output_format short"
  returned: on success for state recently_played
  sample:
    changed: True
    result:
        devices:
        - name: Device1
          device_id: ABC6363f1d95BBCCCDDa95cc67f6307
  type: dict

output:
  description: "returns a dict with the result for state user_info"
  returned: on success for state user_info
  sample:
    changed: True
    result:
        display_name:
        external_urls:
          spotify: https://open.spotify.com/user/USER
        followers:
          href:
          total: 1
        href: https://api.spotify.com/v1/users/USER
        id: USER
        images: []
        type: user
        uri: spotify:user:USER
  type: dict
```
