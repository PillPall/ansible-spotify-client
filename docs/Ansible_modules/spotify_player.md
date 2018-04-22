> SPOTIFY_PLAYER    (./ansible/library/spotify_player.py)

        Ansible module for controlling your spotify. Play or pause a song, toggle shuffle on/off or set the volume.

OPTIONS (= is mandatory):

= auth_token
        Authentication token for Spotify API

        type: String

= device_Id
        Device ID to transfer a User's Playback

        type: String

- repeat_mode
        Set shuffle on or off
        (Choices: track, context, off)[Default: (null)]
        type: String

= state
        Player action to execute
        (Choices: play, pause, next, previous, repeat, shuffle, volume)
        type: String

- toggle_shuffle
        Set shuffle on or off
        (Choices: on, off)[Default: (null)]
        type: String

- volume_level
        Set volume level in percent
        [Default: (null)]
        type: int


REQUIREMENTS:  python >= 2.7.10, spotipy >= 2.4.4

AUTHOR: Michael Bloch (github@mbloch.de)
        METADATA:
          status:
          - preview
          supported_by: community


EXAMPLES:
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

- name: Transfer playback to a new device
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    device_id: 0123456789ABCDEFGHI
    state: transfer_playback

RETURN VALUES:


---
output:
  description: "Returns null."
  returned: on success
  sample:
    changed: True
    result: null
  type: null
