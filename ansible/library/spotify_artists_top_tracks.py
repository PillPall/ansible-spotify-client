#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: spotify_auth_create_user_token
short_description: Ansible module for getting top tracks per country for one artist
description:
    - "Ansible module to get the top trachs for an artists in a specific country. Artists can be provided via name, uri or JSON File
    which gets generated by using the ansible module spotify_search or spotify_related_artists or visit
    https://developer.spotify.com/documentation/web-api/reference/object-model/ for more informations."

version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)

options:
    artists_name:
        description:
          - Artists name to get the related artists for.
        type: String

    artists_uri:
        description:
          - Artists URI to get top tracks for.
        type: String

    artists_file:
        description:
          - JSON File containing a dict of track names.
        type: String

    auth_token:
        description:
          - Spotify authentication token generated from the module spotify_auth and spotify_auth_create_user_token
        required: true
        type: String

    country_code:
        description:
          - Country code to get the top tracks from.
        default: AU
        type: String

    dest_file:
        description:
          - Destination file to save the output to.

    output_format:
        description:
          - Control Ansible output.
        choices: ['short', 'long']
        default: long
        type: String

requirements:
- python >= 2.7.10
- spotipy >= 2.4.4
'''

EXAMPLES = '''
- name: Get top tracks for an named artist in australia and save it to file
  spotify_artists_top_tracks:
    auth_token: 0123456789ABCDEFGHI
    artist_name: young the giant
    country_code: au
    dest_file: artists.json
    output_format: short

- name: Get top tracks for an artists with given URI wi in germany
  spotify_artists_top_tracks:
    auth_token: 0123456789ABCDEFGHI
    artists_uri: spotify:artist:4j56EQDQu5XnL7R3E9iFJT
    country_code: de
    output_format: long
  register: results

- name: Get top tracks for artists via file
  spotify_artists_top_tracks:
    auth_token: 0123456789ABCDEFGHI
    artists_file: "{{ playbook_dir }}/files/related_artists.json"
    output_format: long
  register: results

- name: Example of how to get top tracks for artists found with Ansible module spotify_related_artists
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_name: "Young the Giant"
    dest_file: "{{ playbook_dir }}/files/related_artists.json"

  spotify_artists_top_tracks:
    auth_token: 0123456789ABCDEFGHI
    artists_file: "{{ playbook_dir }}/files/related_artists.json"
    output_format: long
    dest_file: "{{ playbook_dir }}/files/related_artists_top_tracks.json"
'''
RETURN = '''
---
output:
  description: "returns a dict type with the full information or a short descripion about each track."
  returned: on success
  sample:
    changed: True
    result:
        tracks:
            track: Cough Syrup
            uri:spotify:track:4Tfe8Uu9faFdWRiZbpvpXd
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


class ArtistsTopTracks:

    def __init__(self, module):
        self.module = module

        self.client = spotipy.Spotify(self.module.params.get("auth_token"))

    def get_artists_uri(self, artists_name=None):
        if artists_name is None:
            artists_name = self.module.params.get("artists_name")

        result = self.client.search(q='artist:' + artists_name, type='artist')

        try:
            if 'artists' in result:
                if result['items']:
                    artists_uri = result['artists']['items'][0]['uri']
                    self.module.params.update(artists_uri=artists_uri)

        except Exception as e:
            self.module.fail_json(msg="Error: Getting URI for artist" + artist_name + " - " + str(e))

    def get_top_tracks_from_file(self):
        artists_file = self.module.params.get("artists_file")
        tracks_dict = {'tracks': []}

        try:
            artists_from_file = json.load(open(artists_file))
        except Exception as e:
            self.module.fail_json(msg="Error: Can't load artists file" + artists_file + " - " + str(e))

        if isinstance(artists_from_file, dict):
            if 'artists' in artists_from_file:
                if artists_from_file['artists']:
                    for artist in artists_from_file['artists']:
                        result = self.get_top_tracks(artists_uri=artist['uri'])
                        tracks_dict = self.append_to_dict(result, tracks_dict)
            else:
                self.module.fail_json(msg="Error: Can't read dict in file.")
        else:
            self.module.fail_json(msg="Error: Can't file does not type of dict or list.")

        return tracks_dict

    def get_top_tracks(self, artists_uri=None, country_code=None):
        if artists_uri is None:
            artists_uri = self.module.params.get("artists_uri")
        if country_code is None:
            country_code = self.module.params.get("country_code")

        try:
            result = self.client.artist_top_tracks(artists_uri, country_code)
            return result
        except Exception as e:
            self.module.fail_json(msg="Error: Can't get artists top tracks - " + str(e))

    def append_to_dict(self, top_tracks, tracks_dict):
        for artists_top_tracks_list in top_tracks['tracks']:
                if artists_top_tracks_list not in tracks_dict['tracks']:
                    tracks_dict['tracks'].append(artists_top_tracks_list)
        return tracks_dict

    def output_shortener(self, track_list):
        output_shortener_dict = {'tracks': []}
        for track in track_list['tracks']:
            output_shortener_dict['tracks'].append({'track': track['name'], 'uri': track['uri']})
        return output_shortener_dict


def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        artists_uri=dict(required=False, type='str'),
        artists_name=dict(required=False, type='str'),
        artists_file=dict(required=False, type='str'),
        country_code=dict(default='AU', required=False, type='str'),
        output_format=dict(default='long', choices=['short', 'long'], type='str'),
        dest_file=dict(required=False, type='str')
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    output_format = module.params.get("output_format")

    top_tracks = ArtistsTopTracks(module)

    if module.params.get("artists_name"):
        top_tracks.get_artists_uri()

    if module.params.get("artists_file"):
        results = top_tracks.get_top_tracks_from_file()
    else:
        results = top_tracks.get_top_tracks()

    if output_format == 'short':
        results = top_tracks.output_shortener(results)

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, results=results)

if __name__ == '__main__':
    main()
