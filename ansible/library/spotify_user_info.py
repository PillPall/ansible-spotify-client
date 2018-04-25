#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: spotify_user_info
short_description: Ansible module to get informations about the current User.
description:
    - "Ansible module to get different informations about the current user. Following information can you get with this module:
    * current playback
    * Devices
    * Recently played tracks
    * Top Tracks
    * Top Artists
    * User informations

    The options limit and time_range can only defined together with the state recently_played, top_tracks and top_artists.

    The options dest_file and output_format can be combined."

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
         - Limit the output for top artists, top tracks or recently played tracks.
       default: 50
       type: String

   output_format:
       description:
         - Control Ansible output.
       choices: ['short', 'long']
       default: short
       type: String

   state:
       description:
         - User info to get.
       choices: ['current_playback', 'devices', 'recently_played', 'top_tracks', 'top_artists', 'user_info']
       type: String

   time_range:
       description:
         - Time range for seeing users top artists and top tracks
       choices: ['short_term', 'medium_term', 'long_term']
       default: medium_term
       type: String
'''

EXAMPLES = '''
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

'''

RETURN = '''
---
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

    def devices(self):
        return self.client.devices()

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

    def user_info(self):
        return self.client.me()

    def output_shortener(self, results):
        if self.module.params.get("state") == 'current_playback':
            output_dict = {}
            if results:
                output_dict.update({'album': results['item']['album']['name']})
                output_dict.update({'artists': results['item']['artists'][0]['name']})
                output_dict.update({'track': results['item']['name']})
                output_dict.update({'uri': results['item']['uri']})
        elif self.module.params.get("state") == 'recently_played':
            output_dict = ({'tracks': []})
            for tracks in results['items']:
                album = tracks['track']['album']['name']
                artist = tracks['track']['artists'][0]['name']
                track = tracks['track']['name']
                uri = tracks['track']['uri']

                output_dict['tracks'].append({'album': album, 'artists': artist, 'track': track, 'uri': uri})
        elif self.module.params.get("state") == 'top_tracks':
            output_dict = ({'tracks': []})
            for tracks in results['items']:
                album = tracks['album']['name']
                artist = tracks['artists'][0]['name']
                track = tracks['name']
                uri = tracks['uri']

                output_dict['tracks'].append({'album': album, 'artists': artist, 'track': track, 'uri': uri})
        elif self.module.params.get("state") == 'top_artists':
            output_dict = ({'artists': []})
            for artists in results['items']:
                artist = artists['name']
                uri = nartists['uri']

                output_dict['artists'].append({'artists': artist, 'uri': uri})
        elif self.module.params.get("state") == 'user_info':
            output_dict = ({'user_info': []})
            id = results['id']
            uri = results['uri']

            output_dict['user_info'].append({'user_id': id, 'user_uri': uri})
        elif self.module.params.get("state") == 'devices':
            output_dict = ({'devices': []})
            for devices in results['devices']:
                name = devices['name']
                id = devices['id']

                output_dict['devices'].append({'name': name, 'device_id': id})

        return output_dict


def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        output_format=dict(required=False, default='long', choices=['short', 'long'], type='str'),
        dest_file=dict(required=False, type='str'),
        limit=dict(required=False, default=50, type='int'),
        time_range=dict(required=False, default='medium_term', choices=['short_term', 'medium_term', 'long_term'], type='str'),
        state=dict(required=True, choices=['current_playback', 'devices', 'recently_played', 'top_tracks', 'top_artists', 'user_info'])
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
    elif module.params.get("state") == 'devices':
        results = usertrack.devices()
    elif module.params.get("state") == 'user_info':
        results = usertrack.user_info()

    if output_format == 'short':
        results = usertrack.output_shortener(results)

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
