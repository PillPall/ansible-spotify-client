#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: spotify_user_playlists
short_description: Get information about users playlist or create one.
description:
    - "Get information about the current User."
version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)

options:
   auth_token:
       description:
         - Authentication token for Spotify API.
       required: True
       type: String

   dest_file:
       description:
         - Destination file to save the output to.
       type: String

   limit:
       description:
         - Limit the amount of the user playlists to get or to search for.
       default: 50
       type: String

   output_format:
       description:
         - Control Ansible output.
       choices: ['short', 'long']
       default: long
       type: String

   playlist_description:
       description:
         - Playlist description for creating a new playlist.
       default: ""
       type: String

   playlist_name:
       description:
         - Name of the playlist to search for or to create.
       type: String

   public:
       description:
         - Parameter to make a created playlist public or non-public
       default: no
       choices: ['yes', 'no']
       type: String

   state:
       description:
         - Playlist action.
       choices: ['get_all', 'create', 'search']
       type: String

   username:
      description:
        - Create the playlist for the user defined in username.
      type: String
'''

EXAMPLES = '''
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
'''

RETURN = '''
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
'''

import sys
import os
import json

from ansible.module_utils.basic import *

try:
    import spotipy
except ImportError as e:
    module.fail_json(msg="Error: Can't import required libraries - " + str(e))

class UserPlaylist:
    def __init__(self, module):
        self.module = module

        self.client = spotipy.Spotify(self.module.params.get("auth_token"))

    def get_all(self):
        limit = self.module.params.get("limit")

        try:
            result = self.client.current_user_playlists(limit=limit)
            return result
        except Exception as e:
          self.module.fail_json(msg="Error: Can't get user playlists - " + str(e))

    def search(self, playlists_dict):
        playlist_name = self.module.params.get("playlist_name")
        playlist_found_dict = {'items': []}

        for playlist in playlists_dict['items']:
            if playlist_name in playlist['name']:
                playlist_found_dict['items'].append(playlist)

        return playlist_found_dict

    def create(self):
        username = self.module.params.get("username")
        playlist_name = self.module.params.get("playlist_name")

        if self.module.params.get("public") == 'yes':
            public = True
        else:
            public = False

        playlist_description = self.module.params.get("playlist_description")

        try:
            result = self.client.user_playlist_create(username, playlist_name, public, playlist_description)
            return result
        except Exception as e:
          self.module.fail_json(msg="Error: Can't create playlists for user" + username + " - " + str(e))

    def output_shortener(self, playlists_dict):
        output_shortener_dict = {'playlists': []}
        for playlist in playlists_dict['items']:
          output_shortener_dict['playlists'].append({'name': playlist['name'], 'uri': playlist['uri']})
        return output_shortener_dict

def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        dest_file=dict(required=False, type='str'),
        limit=dict(required=False, default=50, type='int'),
        output_format=dict(required=False, default='long', choices=['short', 'long'], type='str'),
        playlist_name=dict(required=False, type='str'),
        playlist_description=dict(required=False, default='', type='str'),
        public=dict(required=False, default='no', choices=['yes', 'no'], type='str'),
        state=dict(required=True, choices=['get_all', 'create', 'search'], type='str'),
        username=dict(required=False, type='str')
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    output_format = module.params.get("output_format")
    state = module.params.get("state")

    playlists = UserPlaylist(module)

    if state == 'get_all':
        results = playlists.get_all()
    elif state == 'create':
        results = playlists.create()
    elif state =='search':
        playlists_get_all = playlists.get_all()
        results = playlists.search(playlists_get_all)

    if output_format == 'short':
        results = playlists.output_shortener(results)

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
