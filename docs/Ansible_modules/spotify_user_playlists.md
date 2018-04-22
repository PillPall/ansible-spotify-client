> SPOTIFY_USER_PLAYLISTS    (./ansible/library/spotify_user_playlists.py)

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
        Limit the amount of the user playlists to get or to search for.
        [Default: 50]
        type: String

- output_format
        Control Ansible output.
        (Choices: short, long)[Default: long]
        type: String

- playlist_description
        Playlist description for creating a new playlist.
        [Default: ]
        type: String

- playlist_name
        Name of the playlist to search for or to create.
        [Default: (null)]
        type: String

- public
        Parameter to make a created playlist public or non-public
        (Choices: yes, no)[Default: False]
        type: String

- state
        Playlist action.
        (Choices: get_all, create, search)[Default: (null)]
        type: String

- username
        Create the playlist for the user defined in username.
        [Default: (null)]
        type: String


AUTHOR: Michael Bloch (github@mbloch.de)
        METADATA:
          status:
          - preview
          supported_by: community


EXAMPLES:
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
    playlist_description: Playlist created with Ansible
    playlist_name: Ansible_Playlist
    public: yes
    state: create

- name: Search in the first 20 User playlists for a Playlist named Ansible_Playlist
  spotify_get_user_playlist:
    auth_token: 0123456789ABCDEFGHI
    limit: 20
    playlist_name: Ansible_Playlist
    state: search

RETURN VALUES:


---
output:
  description: "returns a dict with the snapshot_ids of the updated playlists"
  returned: on success
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
          name: Ansible integration test nonpublic3
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
