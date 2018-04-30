#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: spotify_track_data
short_description: Get detail information about tracks.
description:
    - "Ansible module to get audio features or analysis data from a track.
    For more information see https://beta.developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/ &
    https://beta.developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/.

    Tracks can be provided via URI or JSON File.
    Visit https://developer.spotify.com/documentation/web-api/reference/object-model/ for more informations."
version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)

options:
    auth_token:
        description:
          - Spotify authentication token generated from the module spotify_auth and spotify_auth_create_user_token
        required: True
        type: String

    dest_file:
        description:
          - Destination file to save the output to.
        type: String

    state:
        description:
          - Get track features or analyse a song
        choices: ['feature', 'analyse']
        required: True
        type: String

    track_id:
        description:
          - Track ID or URI to update.
        type: String

    track_file:
        description:
          - JSON File containing a dict of Track IDs or URIs to update.
        type: String

requirements:
- python >= 2.7.10
- spotipy >= 2.4.4
'''


EXAMPLES = '''
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
'''
RETURN = '''
---
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
'''

import sys
import os
import json
from ansible.module_utils.basic import *

try:
    import spotipy
except ImportError as e:
    module.fail_json(msg="Error: Can't import required libraries - " + str(e))

class TrackData:
    def __init__(self, module):
        self.module = module

        self.client = spotipy.Spotify(self.module.params.get("auth_token"))

    def feature(self):
        method_to_call = self.client.audio_features
        ii = 49

        results = self.track_data_looper(method_to_call, ii)

        return results

    def analyse(self):
        method_to_call = self.client.audio_analysis
        ii = 1

        results = self.track_data_looper(method_to_call, ii)

        return results

    def track_data_looper(self, method_caller, ii):
        tracks_dict = self.create_tracks_dict()
        track_dict_list_length = len(tracks_dict['tracks'])
        results = {'result': []}
        i = 0
        iii = ii
        done = False

        while not done:
            if self.module.params.get("state") == 'analyse':
                track = tracks_dict['tracks'][i]
            else:
                track = tracks_dict['tracks'][i:track_dict_list_length]

            if track_dict_list_length == 1:
                if self.module.params.get("state") == 'analyse':
                    track = tracks_dict['tracks'][0]
                else:
                    track = [tracks_dict['tracks'][0]]

                try:
                    result = method_caller(track)
                    results['result'].append(result)
                except Exception as e:
                    self.module.fail_json(msg="Error: Can't get track" + self.module.params.get("state") + "  - " + str(e))
                done = True
            elif ii == track_dict_list_length:
                try:
                    result = method_caller(track)
                    results['result'].append(result)
                except Exception as e:
                    self.module.fail_json(msg="Error: Can't get track" + self.module.params.get("state") + "  - " + str(e))
                done = True
            elif ii > track_dict_list_length:
                try:
                    result = method_caller(track)
                    results['result'].append(result)
                except Exception as e:
                    self.module.fail_json(msg="Error: Can't get track" + self.module.params.get("state") + "  - " + str(e))
                done = True
            while ii < track_dict_list_length:

                try:
                    result = method_caller(track)
                    results['result'].append(result)
                except Exception as e:
                    self.module.fail_json(msg="Error: Can't get track" + self.module.params.get("state") + "  - " + str(e))
                i = i + iii
                ii = ii + iii
                done = False

        return results

    def create_tracks_dict(self):
        if self.module.params.get("track_id"):
            tracks_dict = {'tracks': []}
            tracks_dict['tracks'].append(self.module.params.get("track_id"))
        elif self.module.params.get("track_file"):
            track_file = self.module.params.get("track_file")
            tracks_dict = self.get_tracks_from_file(track_file)
        else:
            self.module.fail_json(msg="Error: No Track ID or file was given")

        return tracks_dict

    def get_tracks_from_file(self, track_file):
        tracks_dict = {'tracks': []}

        try:
            track_from_file = json.load(open(track_file))
        except Exception as e:
            self.module.fail_json(msg="Error: Can't load track file" + track_file + " - " + str(e))

        try:
            if 'tracks' in track_from_file:
                if track_from_file['tracks']:
                    for track in track_from_file['tracks']:
                        tracks_dict['tracks'].append(track['uri'])
            elif 'items' in track_from_file:
                if track_from_file['items']:
                    for track in track_from_file['items']:
                        tracks_dict['tracks'].append(track['uri'])
            elif 'type' in track_from_file:
                if track_from_file['type'] == 'track':
                        tracks_dict['tracks'].append(track_from_file['uri'])
        except Exception as e:
            self.module.fail_json(msg="Error: Can't read dict in tracks file. - " + str(e))

        return tracks_dict
def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        dest_file=dict(required=False, type='str'),
        state=dict(required=True, choices=['analyse', 'feature'], type='str'),
        track_id=dict(required=False, type='str'),
        track_file=dict(required=False, type='str')
    ))
    module = AnsibleModule(argument_spec=argument_spec)
    state = module.params.get("state")

    track_data = TrackData(module)

    if state == 'feature':
        results = track_data.feature()
    elif state == 'analyse':
        results = track_data.analyse()

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
