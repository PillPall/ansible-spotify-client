> SPOTIFY_UPDATE_PLAYLISTS    (./ansible/library/spotify_update_playlists.py)

        Ansible module to add or remove tracks to/from a user playlist. Tracks and playlists can be provided via a JSON File. Visit
        https://developer.spotify.com/documentation/web-api/reference/object-model/ for more informations.

OPTIONS (= is mandatory):

= auth_token
        Spotify API authentication token

        type: String

- dest_file
        Path to file to save the search result.
        [Default: (null)]
        type: String

- playlist_file
        JSON File containing a dict of Playlist ID or URI to update. Fore more information about the JSON structure visit
        https://beta.developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/.
        [Default: (null)]
        type: String

- playlist_id
        Playlist ID or URI to update.
        [Default: (null)]
        type: String

= state
        Add or remove tracks from playlist
        (Choices: add, remove)
        type: String

- track_file
        JSON File containing a dict of Track IDs or URIs to update. Fore more information about the JSON structure visit
        https://beta.developer.spotify.com/documentation/web-api/reference/artists/get-artists-top-tracks/.
        [Default: (null)]
        type: String

- track_id
        Track ID or URI to update.
        [Default: (null)]
        type: String

= username
        Username to update the playlist for

        type: String


REQUIREMENTS:  python >= 2.7.10, spotipy >= 2.4.4

AUTHOR: Michael Bloch (github@mbloch.de)
        METADATA:
          status:
          - preview
          supported_by: community


EXAMPLES:
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

- name: Example of how to use spotify_artists_top_tracks module to update a playlist
  spotify_artists_top_tracks:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_name: "Young the Giant"
    dest_file: "{{ playbook_dir }}/files/tracks.json"

- name: Add songs to playlist
  spotify_update_playlists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    username: "USER"
    state: "add"
    playlist_id: spotify:user:USER:playlist:BCASDJLASDKV12345
    track_file: "{{ playbook_dir }}/files/tracks.json"

RETURN VALUES:


---
output:
  description: "returns a dict with the snapshot_ids of the updated playlists"
  returned: on success
  sample:
    changed: True
    result:
        snapshot_id: 4HJAHdr2BypGxe/esgasdfihIMcv4luhnZlAhGXL295BefUSisFtRjl0D8CxGqaVrY
  type: dict
