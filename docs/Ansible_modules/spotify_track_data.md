# Spotify track data

#### Modules
spotify_track_data - Get detail information about tracks.

* Synopsis
* Options
* Examples
* Return value

#### Synopsis

Ansible module to get audio features or analysis data from a track.
For more informations see [Audio features](https://beta.developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/) &
[Audio analysis](https://beta.developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/).

Tracks can be provided via *URI or JSON File**. A JSON file can be generated using the Ansible module `spotify_search` or `spotify_artists_top_tracks`.

For more informations about the JSON data structure visit this link [(link tracks)](https://beta.developer.spotify.com/documentation/web-api/reference/tracks/get-several-tracks/).

You can only define one of the `track_id` and `track_file` options.

The option `dest_file` can be combined with all states.

#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------  |----------- |--------- | -------- |
| auth_token  | String        | Yes        | null       | null     | Spotify authentication token generated from the module `spotify_auth` and `spotify_auth_create_user_token` |
| state         | String      | Yes        | null | analyse, feature | Add or remove tracks from playlist |
| track_id      | String       | No        | null       | null     |  Track ID or URI to update. |
| track_file    | String       | No        | null       | null     |  JSON File containing a dict of Track IDs or URIs to update. |
| dest_file     | String       | No        | null       | null     |  Destination file to save the output to. |


#### Requirements  
* python >= 2.7.10
* spotipy >= 2.4.4

#### Examples
```
- name: Get track features from track id
  spotify_track_data:
    auth_token: "{{ auth_token }}"
    state: feature
    track_id: spotify:track:4Sfa7hdVkqlM8UW5LsSY3F

- name: Get track features from track file with defined dest_file
  spotify_track_data:
    auth_token: "{{ auth_token }}"
    state: feature
    track_file: "{{ playbook_dir }}/../files/user_top_tracks.json"
    dest_file: "{{ playbook_dir }}/../files/track_data_{{ track_data_state }}.json"

- name: Analyse track from track id
  spotify_track_data:
    auth_token: "{{ auth_token }}"
    state: analyse
    track_id: spotify:track:4Sfa7hdVkqlM8UW5LsSY3F

- name: Analyse track from track file with defined dest_file
  spotify_track_data:
    auth_token: "{{ auth_token }}"
    state: analyse
    track_file: "{{ playbook_dir }}/../files/user_top_tracks.json"
    dest_file: "{{ playbook_dir }}/../files/track_data_{{ track_data_state }}.json"
```

#### RETURN VALUES:
```
output:
description: "returns a dict with the track feature data"
 returned: on success
 sample:
   changed: True
   result:
       track_href: https://api.spotify.com/v1/tracks/5eG8mKV70BVABCSqSy4tKp
       analysis_url: https://api.spotify.com/v1/audio-analysis/5eG8mKV70BVABCSqSy4tKp
       energy: 0.28
       liveness: 0.266
       tempo: 133.763
       speechiness: 0.0301
       uri: spotify:track:5eG8mKV70BVABCSqSy4tKp
       acousticness: 0.301
       instrumentalness: 0.000426
       time_signature: 4
       danceability: 0.504
       key: 11
       duration_ms: 246427
       loudness: -9.557
       valence: 0.255
       type: audio_features
       id: 5eG8mKV70BVABCSqSy4tKp
       mode: 1
 type: dict

 output:
   description: "returns a dict with the track analysing data"
   returned: on success
   sample:
     changed: True
     result:
        [...]
   type: dict
```
