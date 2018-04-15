#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1'}
DOCUMENTATION = '''
---
module: spotify_get_user_playlist
Ansible module for getting related artists for one artist
requirements:
  - python >= 2.6
 - spotipy >= 2.4.4
options:
    username:
        description:
          - Username to get the playlist from
        required: True
        type: String
   dest_file:
       description:
         - Destination file to save the output to
   output_format:
       description:
         - Output format
       Default: short
       type: String
       Choices: short, full
   auth_token:
       description:
         - Authentication token for Spotify API
       required: True
       type: String
'''

EXAMPLES = '''
- name: Get user playlists for user muster and save to dest_file
  spotify_get_user_playlist:
    auth_token=0123456789ABCDEFGHI
    username: muster
    dest_file=artists.json
    output_format=short
'''


import sys
import os
import json
from ansible.module_utils.basic import *

try:
    import spotipy_connection
except ImportError as e:
    module.fail_json(msg="Error: Can't import required libraries - " + str(e))

class UserPlaylist:
    def __init__(self, module):
        self.module = module
        self.playlists_list = []

        self.client = spotipy_connection.client(self.module)

    def get(self):
        username = self.module.params.get("username")

        try:
            result = self.client.user_playlists(username)
            return result
        except Exception as e:
          self.module.fail_json(msg="Error: Can't get playlists for user" + username + " - " + str(e))

    def create(self):
        username = self.module.params.get("username")
        playlist_name = self.module.params.get("playlist_name")

        if self.module.params.get("public") == 'yes':
            public = True
        else:
            public = False

        if self.module.params.get("playlist_description"):
            playlist_description = self.module.params.get("playlist_description")
        else:
            playlist_description = ''

        try:
            result = self.client.user_playlist_create(username, playlist_name, public, playlist_description)
            return result
        except Exception as e:
          self.module.fail_json(msg="Error: Can't create playlists for user" + username + " - " + str(e))

    def playlists_to_list(self, playlists_dict):
        for playlist in playlists_dict['items']:
          self.playlists_list.append(playlist['name'])
        return self.playlists_list

def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        username=dict(required=True, type='str'),
        output_format=dict(required=False, default='short', choices=['short', 'full'], type='str'),
        dest_file=dict(required=False, type='str'),
        state=dict(required=True, choices=['get', 'create'], type='str'),
        playlist_name=dict(required=False, type='str'),
        public=dict(required=False, default='no', choices=['yes', 'no'], type='str')
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    output_format = module.params.get("output_format")
    state = module.params.get("state")

    playlists = UserPlaylist(module)

    if state == 'get':
        playlists_dict = playlists.get()
        if output_format == 'short':
            results = playlists.playlists_to_list(playlists_dict)
        else:
            results = playlists_dict
    elif state == 'create':
        results = playlists.create()

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
