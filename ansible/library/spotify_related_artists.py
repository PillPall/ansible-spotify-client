#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1'}
DOCUMENTATION = '''
---
module: spotify_related_artists
Ansible module for getting related artists for one artist with spotipy
requirements:
  - python >= 2.6
  - spotipy >= 2.4.4
options:
    artists_name:
        description:
          - Artists name to get the related artists for
        type: String
    artists_file:
        description:
          - JSON File with artists names. JSON File can be a list of artists name or a dict
            see https://developer.spotify.com/web-api/get-related-artists/
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
- name: Get related artists name for young the giant and save it to file
  spotify_related_artists:
    auth_token=0123456789ABCDEFGHI
    artists_name=young the giant
    dest_file=artists.json
    output_format=short

- name: Get related artists for young the giant
  spotify_related_artists:
    auth_token=0123456789ABCDEFGHI
    artists_name=young the giant
    output_format=long
  register: results

 - name: Get related artists for artists from file:
   spotify_related_artists:
     auth_token=0123456789ABCDEFGHI
     artists_file="/tmp/artists.json"
     output_format=long
   register: results

'''

import sys
import os
import json
from ansible.module_utils.basic import *

try:
    import spotipy
except ImportError as e:
    module.fail_json(msg="Error: Can't import required libraries - " + str(e))

class RelatedArtists:
    def __init__(self, module):
        self.module = module

        self.client = spotipy.Spotify(self.module.params.get("auth_token"))

    def get_related_from_file(self):
        artists_file = self.module.params.get("artists_file")
        artists_dict = {'artists': []}

        try:
            artists_from_file = json.load(open(artists_file))
        except Exception as e:
          self.module.fail_json(msg="Error: Can't load artists file" + artists_file + " - " + str(e))

        if isinstance(artists_from_file, dict):
            if artists_from_file['artists'][0]['name']:
                for artist in artists_from_file['artists']:
                    result_related_artists = self.get_related_for_artists(artist['name'])
                    artists_dict = self.append_to_dict(result_related_artists, artists_dict)
            else:
                self.module.fail_json(msg="Error: Can't read dict in artists file. See https://developer.spotify.com/web-api/get-related-artists/ for a correct dict structure." )

        elif isinstance(artists_from_file, list):
            try:
                for artist in artists_from_file:
                    result_related_artists = self.get_related_for_artists(artist)
                    artists_dict = self.append_to_dict(result_related_artists, artists_dict)
            except Exception as e:
              self.module.fail_json(msg="Error: Can't read list in artists file. List can only contain artists name - " + str(e))
        else:
            self.module.fail_json(msg="Error: Can't file does not type of dict or list.")

        return artists_dict

    def get_related_for_artists(self, artists_name=None):
        if artists_name is None:
            artists_name = self.module.params.get("artists_name")

        result = self.client.search(q='artist:' + artists_name, type='artist')

        try:
          uri = result['artists']['items'][0]['uri']

          result_related_artists = self.client.artist_related_artists(uri)

          return result_related_artists

        except Exception as e:
          self.module.fail_json(msg="Error: Can't get results for related artists - " + str(e))

    def append_to_dict(self, related_artists, artists_dict):
        for related_artists_name_list in related_artists['artists']:
                if related_artists_name_list not in artists_dict['artists']:
                    artists_dict['artists'].append(related_artists_name_list)
        return artists_dict

    def name_to_list(self, artists_dict):
        artists_name_dict_short = {'artists': []}
        for artist in artists_dict['artists']:
          artists_name_dict_short['artists'].append({'artist': artist['name'], 'uri': artist['uri']})
        return artists_name_dict_short

def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        artists_name=dict(required=False, type='str'),
        artists_file=dict(required=False, type='str'),
        dest_file=dict(required=False, type='str'),
        output_format=dict(default='full', choices=['short', 'full'], type='str')
    ))
    module = AnsibleModule(argument_spec=argument_spec)

    output_format = module.params.get("output_format")

    artists = RelatedArtists(module)

    if module.params.get("artists_file"):
        results = artists.get_related_from_file()
    else:
        results = artists.get_related_for_artists()

    if output_format == 'short':
        results = artists.name_to_list(results)

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
