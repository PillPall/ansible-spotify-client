#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: spotify_related_artists
short_description: Ansible module to get 20 related artists for a given artists.
description:
    - "Ansible module to get 20 related artists for a given artists. Artists can be provided via name or JSON Fil.
    A JSON file can be generated using the Ansible module spotify_search or visit this site for more informations https://beta.developer.spotify.com/documentation/web-api/reference/artists/get-artist/.

    You can only define one of the options at the same time: artists_name or artists_file.
    The options dest_file and output_format can be combined."

version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)

options:
    artists_name:
        description:
          - Artists name to get the related artists for.
        type: String

    artists_file:
        description:
          - JSON File containing a dict of track names.
        type: String

    auth_token:
        description:
          - Spotify authentication token generated from the module spotify_auth and spotify_auth_create_user_token
        required: True
        type: String

    dest_file:
        description:
          - Destination file to save the output to.
        type: String

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
- name: Get related artists name for young the giant with output_format short
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_name: young the giant
    output_format: short

- name: Get related artists name for young the giant with output_format long and save output
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_name: young the giant
    output_format: long
    dest_file: "{{ playbook_dir }}/files/related_artists.json"

- name: Get related artists from file
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_file: "{{ get_related_artists_from_file }}"

- name: Get related artists from file and save output
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_file: "{{ get_related_artists_from_file }}"
    dest_file: "{{ playbook_dir }}/files/related_artists.json"

#
# Example of how to use spotify_related_artists for a nested usage
#
- name: Get related artists for Young the giant
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_name: "Young the Giant"
    dest_file: "{{ playbook_dir }}/files/related_artists.json"

- name: Get related artists for related artists for Young the giant
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_file: "{{ playbook_dir }}/files/related_artists.json"
    dest_file: "{{ playbook_dir }}/files/related_artists.json"
'''
RETURN = '''
---
output:
  description: "Returns a dict with informations about the related artists with defined output_format short.
  returned: on success
  sample:
    changed: True
    result:
      artists:
      - uri: spotify:artist:54QMjE4toDfiCryzYWCpXX
        artist: Metronomy
      - uri: spotify:artist:6FQqZYVfTNQ1pCqfkwVFEa
        artist: Foals
  type: dict

output:
  description: "Returns a dict with informations about the related artists  with defined output_format long.
  returned: on success
  sample:
    changed: True
    result:
        artists:
            - external_urls:
                spotify: https://open.spotify.com/artist/3kVUvbeRdcrqQ3oHk5hPdx
              followers:
                href:
                total: 602082
              genres:
              - indie folk
              - indie pop
              - indie rock
              - indietronica
              - la indie
              - modern rock
              - shimmer pop
              - stomp and holler
              - synthpop
              href: https://api.spotify.com/v1/artists/3kVUvbeRdcrqQ3oHk5hPdx
              id: 3kVUvbeRdcrqQ3oHk5hPdx
              images:
              - height: 640
                url: https://i.scdn.co/image/0763ebd8606dc0a33984b7901ebdd9966d79ff24
                width: 640
              - height: 320
                url: https://i.scdn.co/image/9d6b9d1f5800063806d429bec4ad13794d548659
                width: 320
              - height: 160
                url: https://i.scdn.co/image/6463aca37297e74b497fe04cdaa00c9b87a11492
                width: 160
              name: Grouplove
              popularity: 69
              type: artist
              uri: spotify:artist:3kVUvbeRdcrqQ3oHk5hPdx
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


class RelatedArtists:
    def __init__(self, module):
        self.module = module

        self.client = spotipy.Spotify(self.module.params.get("auth_token"))

    def get_artists_from_file(self):
        artists_file = self.module.params.get("artists_file")
        artists_dict = {'artists': []}

        try:
            artists_from_file = json.load(open(artists_file))
        except Exception as e:
            self.module.fail_json(msg="Error: Can't load artists file" + artists_file + " - " + str(e))
        if isinstance(artists_from_file, dict):
            if 'artists' in artists_from_file:
                if artists_from_file['artists']:
                    if 'name' in artists_from_file['artists']:
                        if artists_from_file['artists']['name']:
                            for artist in artists_from_file['artists']:
                                result_related_artists = self.get_related_for_artists(artist['name'])
                                artists_dict = self.append_to_dict(result_related_artists, artists_dict)
                    elif 'artist' in artists_from_file['artists']:
                        if artists_from_file['artists']['artist']:
                            for artist in artists_from_file['artists']:
                                result_related_artists = self.get_related_for_artists(artist['artist'])
                                artists_dict = self.append_to_dict(result_related_artists, artists_dict)
                    elif 'artists' in artists_from_file['artists']:
                        if artists_from_file['artists']['artists']:
                            for artist in artists_from_file['artists']:
                                result_related_artists = self.get_related_for_artists(artist['artists'])
                                artists_dict = self.append_to_dict(result_related_artists, artists_dict)
                    elif 'items' in artists_from_file['artists']:
                        if artists_from_file['artists']['items']:
                            for artist in artists_from_file['artists']['items']:
                                result_related_artists = self.get_related_for_artists(artist['name'])
                                artists_dict = self.append_to_dict(result_related_artists, artists_dict)
                    else:
                        for artist in artists_from_file['artists']:
                            if 'artist' in artist:
                                if artist['artist']:
                                    result_related_artists = self.get_related_for_artists(artist['artist'])
                                    artists_dict = self.append_to_dict(result_related_artists, artists_dict)
                            else:
                                self.module.fail_json(msg="Error: Can't read dict in artists file.")
            else:
                self.module.fail_json(msg="Error: Can't read dict in artists file.")

        elif isinstance(artists_from_file, list):
            try:
                for artist in artists_from_file:
                    result_related_artists = self.get_related_for_artists(artist)
                    artists_dict = self.append_to_dict(result_related_artists, artists_dict)
            except Exception as e:
                self.module.fail_json(msg="Error: Can't read list in artists file. List can only contain artists name - " + str(e))
        else:
            self.module.fail_json(msg="Error: File is not type of dict or list.")

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

    def output_shortener(self, artists_dict):
        output_shortener_dict = {'artists': []}
        for artist in artists_dict['artists']:
            output_shortener_dict['artists'].append({'artist': artist['name'], 'uri': artist['uri']})
        return output_shortener_dict


def main():
    argument_spec = {}
    argument_spec.update(dict(
        artists_name=dict(required=False, type='str'),
        artists_file=dict(required=False, type='str'),
        auth_token=dict(required=True, type='str'),
        dest_file=dict(required=False, type='str'),
        output_format=dict(default='long', choices=['short', 'long'], type='str')
    ))
    module = AnsibleModule(argument_spec=argument_spec)

    output_format = module.params.get("output_format")

    artists = RelatedArtists(module)

    if module.params.get("artists_file"):
        results = artists.get_artists_from_file()
    else:
        results = artists.get_related_for_artists()

    if output_format == 'short':
        results = artists.output_shortener(results)

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
