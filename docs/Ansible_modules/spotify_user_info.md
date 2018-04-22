> SPOTIFY_USER_INFO    (./ansible/library/spotify_user_info.py)

        Get information about the current User.

OPTIONS (= is mandatory):

= auth_token
        Authentication token for Spotify API.

        type: String

- dest_file
        Destination file to save the output to.
        [Default: (null)]
        type: String

- limit
        Limit the output for top artists, top tracks or recently played tracks.
        [Default: 50]
        type: String

- output_format
        Control Ansible output.
        (Choices: short, long)[Default: short]
        type: String

- state
        User info to get.
        (Choices: current_playback, devices, recently_played, top_tracks, top_artists, user_info)[Default: (null)]
        type: String

- time_range
        Time range for seeing users top artists and top tracks
        (Choices: short_term, medium_term, long_term)[Default: short]
        type: String


AUTHOR: Michael Bloch (github@mbloch.de)
        METADATA:
          status:
          - preview
          supported_by: community


EXAMPLES:
- name: Get infos about users current playback and save it to a file
  spotify_user_info:
    auth_token: 0123456789ABCDEFGHI
    dest_file: "{{ playbook_dir }}/files/current_user_playback.json"
    state: current_playback

- name: Get all available devies for a user
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

RETURN VALUES:


---
output:
  description: "returns a dict with the result for each state"
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
