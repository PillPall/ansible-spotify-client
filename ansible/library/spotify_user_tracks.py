#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1'}
DOCUMENTATION = '''
---
module: spotify_user_info
Ansible module for getting related artists for one artist
requirements:
  - python >= 2.6
 - spotipy >= 2.4.4
options:
   auth_token:
       description:
         - Authentication token for Spotify API
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
    username:
        description:
          - Username to get the playlist from
        required: True
        type: String
'''

EXAMPLES = '''
- name: Get user info for user muster and save to dest_file
  spotify_user_info:
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
    import spotipy
except ImportError as e:
    module.fail_json(msg="Error: Can't import required libraries - " + str(e))

class UserTracks:
    def __init__(self, module):
        self.module = module

        self.client = spotipy.Spotify(self.module.params.get("auth_token"))

    def current_playback(self):
        return self.client.current_playback()

    def recently_played(self):
        limit = self.module.params.get("limit")
        return self.client.current_user_recently_played(limit=limit)

    def top_tracks(self):
        limit = self.module.params.get("limit")
        time_range = self.module.params.get("time_range")
        return self.client.current_user_top_tracks(limit=limit, time_range=time_range)

    def top_artists(self):
        limit = self.module.params.get("limit")
        time_range = self.module.params.get("time_range")
        return self.client.current_user_top_artists(limit=limit, time_range=time_range)

    def short(self, results):
        if self.module.params.get("state") == 'current_playback':
            output_dict = {}
            output_dict.update({'album': results['item']['album']['name']})
            output_dict.update({'artists': results['item']['artists'][0]['name']})
            output_dict.update({'track': results['item']['name']})
            output_dict.update({'uri': results['item']['uri']})
        elif self.module.params.get("state") == 'recently_played':
            output_dict = ({'recently_played': []})
            for recently_played in results['items']:
                output_dict['recently_played'].append({'album': recently_played['track']['album']['name'], 'artists': recently_played['track']['artists'][0]['name'], 'track': recently_played['track']['name'], 'uri': recently_played['track']['uri']})
        elif self.module.params.get("state") == 'top_tracks':
            output_dict = ({'top_tracks': []})
            for top_tracks in results['items']:
                output_dict['top_tracks'].append({'album': top_tracks['album']['name'], 'artists': top_tracks['artists'][0]['name'], 'track': top_tracks['name'], 'uri': top_tracks['uri']})
        elif self.module.params.get("state") == 'top_artists':
            output_dict = ({'top_artists': []})
            for top_artists in results['items']:
                output_dict['top_artists'].append({'artists': top_artists['name'], 'uri': top_artists['uri']})
        return output_dict

def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        output_format=dict(required=False, default='full', choices=['short', 'full'], type='str'),
        dest_file=dict(required=False, type='str'),
        limit=dict(required=False, default=50, type='int'),
        time_range=dict(required=False, default='medium_term', choices=['short_term', 'medium_term', 'long_term'] , type='str'),
        state=dict(required=True, choices=['current_playback', 'recently_played', 'top_tracks', 'top_artists'])
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    output_format = module.params.get("output_format")

    usertrack = UserTracks(module)

    if module.params.get("state") == 'current_playback':
        results = usertrack.current_playback()
    elif module.params.get("state") == 'recently_played':
        results = usertrack.recently_played()
    elif module.params.get("state") == 'top_tracks':
        results = usertrack.top_tracks()
    elif module.params.get("state") == 'top_artists':
        results = usertrack.top_artists()

    if output_format == 'short':
        results = usertrack.short(results)

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
