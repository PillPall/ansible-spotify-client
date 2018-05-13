#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: spotify_album
short_description: Ansible module to query for album information
description:
    - "Ansible module to query for all album information or only album tracks. Albums can be provided via **URI or JSON File**.

    A JSON file can be generated using the Ansible module `spotify_search`. For more informaiton visit this link (link)](https://beta.developer.spotify.com/documentation/web-api/reference/object-model/#album-object-simplified).

    You can only define one of the option album_file and album_uri options.

    The options dest_file, limit and output_format can be combined with all states.

    Informations about the output format can be found here https://beta.developer.spotify.com/documentation/web-api/reference/albums/get-albums-tracks/."

version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)

options:

    album_file:
        description:
          - JSON File containing a dict of album URIs.
        type: String

    album_uri:
        description:
          - Album Spotify URI
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

    limit:
        description:
          - Limit the search output
        default: 10
        type: Integer

    output_format:
        description:
          - Control Ansible output.
        choices: ['short', 'long']
        default: long
        type: String

    state:
        description:
          - Search to trigger.
        choices: ['album', 'album_tracks']
        required: true
        type: String

requirements:
- python >= 2.7.10
- spotipy >= 2.4.4
'''

EXAMPLES = '''
- name: Get information about an album and return only the first 10 tracks.
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: short
    state: album
    album_uri: 4aawyAB9vmqN3uQ7FjRGTy
    limit: 10
  register: album_information

- name: Get all album tracks.
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: long
    state: album_tracks
    album_uri: 4aawyAB9vmqN3uQ7FjRGTy
  register: album_tracks

- name: Get all album informations from all albums given with a file.
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: short
    state: album
    album_file: "{{playbook_dir}}/search_result_artists_albums.json"
  register: album_information

- name: Get all album tracks from all albums given with a file.
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: long
    state: album_tracks
    album_file: "{{playbook_dir}}/search_result_artists_albums.json"
  register: album_tracks
'''
RETURN = '''
---
output:
  description: "returns a dict with all information about an album long output"
  returned: on success
  sample:
    changed: True
    result:
        album_type: album
            artists:
            - external_urls:
                spotify: https://open.spotify.com/artist/3zD5liDjbqljSRorrrcEjs
              href: https://api.spotify.com/v1/artists/3zD5liDjbqljSRorrrcEjs
              id: 3zD5liDjbqljSRorrrcEjs
              name: Guillemots
              type: artist
              uri: spotify:artist:3zD5liDjbqljSRorrrcEjs
            available_markets:
            - AD
            - AR
            - AT
            - AU
            - BE
            - BG
            - BO
            - BR
            - CA
            - CH
            - CL
            - CO
            - CR
            - CY
            - CZ
            - DE
            - DK
            - DO
            - EC
            - EE
            - ES
            - FI
            - FR
            - GB
            - GR
            - GT
            - HK
            - HN
            - HU
            - ID
            - IE
            - IL
            - IS
            - IT
            - JP
            - LI
            - LT
            - LU
            - LV
            - MC
            - MT
            - MX
            - MY
            - NI
            - NL
            - 'NO'
            - NZ
            - PA
            - PE
            - PH
            - PL
            - PT
            - PY
            - RO
            - SE
            - SG
            - SK
            - SV
            - TH
            - TR
            - TW
            - US
            - UY
            - VN
            - ZA
            copyrights:
            - text: 2012 The state51 Conspiracy Ltd
              type: C
            - text: 2012 The state51 Conspiracy Ltd
              type: P
            external_ids:
              upc: '5055453648229'
            external_urls:
              spotify: https://open.spotify.com/album/1NAThLIEnLUCWXAQLWVxnR
            genres: []
            href: https://api.spotify.com/v1/albums/1NAThLIEnLUCWXAQLWVxnR
            id: 1NAThLIEnLUCWXAQLWVxnR
            images:
            - height: 640
              url: https://i.scdn.co/image/bf5c7e8afcf369da44657b2c1dd1a3cb657608b4
              width: 640
            - height: 300
              url: https://i.scdn.co/image/a19086f9263c84c1f276bb89949534064f63800f
              width: 300
            - height: 64
              url: https://i.scdn.co/image/36c8ae4e633ff8d55422ed1f0ff7f710c53c0462
              width: 64
            label: The state51 Conspiracy
            name: Hello Land!
            popularity: 19
            release_date: '2012-05-08'
            release_date_precision: day
            tracks:
              href: https://api.spotify.com/v1/albums/1NAThLIEnLUCWXAQLWVxnR/tracks?offset=0&limit=50
              items:
              [...]
              - artists:
                - external_urls:
                    spotify: https://open.spotify.com/artist/3zD5liDjbqljSRorrrcEjs
                  href: https://api.spotify.com/v1/artists/3zD5liDjbqljSRorrrcEjs
                  id: 3zD5liDjbqljSRorrrcEjs
                  name: Guillemots
                  type: artist
                  uri: spotify:artist:3zD5liDjbqljSRorrrcEjs
                available_markets:
                - AD
                - AR
                - AT
                - AU
                - BE
                - BG
                - BO
                - BR
                - CA
                - CH
                - CL
                - CO
                - CR
                - CY
                - CZ
                - DE
                - DK
                - DO
                - EC
                - EE
                - ES
                - FI
                - FR
                - GB
                - GR
                - GT
                - HK
                - HN
                - HU
                - ID
                - IE
                - IL
                - IS
                - IT
                - JP
                - LI
                - LT
                - LU
                - LV
                - MC
                - MT
                - MX
                - MY
                - NI
                - NL
                - 'NO'
                - NZ
                - PA
                - PE
                - PH
                - PL
                - PT
                - PY
                - RO
                - SE
                - SG
                - SK
                - SV
                - TH
                - TR
                - TW
                - US
                - UY
                - VN
                - ZA
                disc_number: 1
                duration_ms: 366786
                explicit: false
                external_urls:
                  spotify: https://open.spotify.com/track/59rLnKec0He0mSt9PxmNoU
                href: https://api.spotify.com/v1/tracks/59rLnKec0He0mSt9PxmNoU
                id: 59rLnKec0He0mSt9PxmNoU
                is_local: false
                name: I Lie Down
                preview_url: https://p.scdn.co/mp3-preview/b02526e8b5a9b3dd70edfaa51911668c5e7b058e?cid=a430d21d72594499a3aaee8dc9636a3f
                track_number: 8
                type: track
                uri: spotify:track:59rLnKec0He0mSt9PxmNoU
              limit: 50
              next: null
              offset: 0
              previous: null
              total: 8
            type: album
            uri: spotify:album:1NAThLIEnLUCWXAQLWVxnR
  type: dict

output:
  description: "returns a dict with all information about an album short output"
  returned: on success
  sample:
    changed: True
    result:
        album:
            - name: Global Warming
              uri: spotify:album:4aawyAB9vmqN3uQ7FjRGTy
            artists:
            - name: Pitbull
              uri: spotify:artist:0TnOYISbd1XYRBk9myaseg
            tracks:
            - artists:
              - artists:
                - name: Pitbull
                  uri: spotify:artist:0TnOYISbd1XYRBk9myaseg
                - name: Sensato
                  uri: spotify:artist:7iJrDbKM5fEkGdm5kpjFzS
              track: Global Warming
              uri: spotify:track:6OmhkSOpvYBokMKQxpIGx2
  type: dict

output:
  description: "returns a dict with all tracks from one album in long output format"
  returned: on success
  sample:
    changed: True
    result:
        href: https://api.spotify.com/v1/albums/4aawyAB9vmqN3uQ7FjRGTy/tracks?offset=0&limit=50
            items:
            - artists:
              - external_urls:
                  spotify: https://open.spotify.com/artist/0TnOYISbd1XYRBk9myaseg
                href: https://api.spotify.com/v1/artists/0TnOYISbd1XYRBk9myaseg
                id: 0TnOYISbd1XYRBk9myaseg
                name: Pitbull
                type: artist
                uri: spotify:artist:0TnOYISbd1XYRBk9myaseg
              - external_urls:
                  spotify: https://open.spotify.com/artist/7iJrDbKM5fEkGdm5kpjFzS
                href: https://api.spotify.com/v1/artists/7iJrDbKM5fEkGdm5kpjFzS
                id: 7iJrDbKM5fEkGdm5kpjFzS
                name: Sensato
                type: artist
                uri: spotify:artist:7iJrDbKM5fEkGdm5kpjFzS
              available_markets: []
              disc_number: 1
              duration_ms: 85400
              explicit: true
              external_urls:
                spotify: https://open.spotify.com/track/6OmhkSOpvYBokMKQxpIGx2
              href: https://api.spotify.com/v1/tracks/6OmhkSOpvYBokMKQxpIGx2
              id: 6OmhkSOpvYBokMKQxpIGx2
              is_local: false
              name: Global Warming
              preview_url: null
              track_number: 1
              type: track
              uri: spotify:track:6OmhkSOpvYBokMKQxpIGx2
            [...]
          limit: 50
          next: null
          offset: 0
          previous: null
          total: 18
  type: dict

output:
  description: "returns a dict with all tracks from one album in long output format"
  returned: on success
  sample:
    changed: True
    result:
        tracks:
            - artists:
              - artists:
                - name: Pitbull
                  uri: spotify:artist:0TnOYISbd1XYRBk9myaseg
                - name: Sensato
                  uri: spotify:artist:7iJrDbKM5fEkGdm5kpjFzS
              track: Global Warming
              uri: spotify:track:6OmhkSOpvYBokMKQxpIGx2
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


class SpotifySearch:
    def __init__(self, module):
        self.module = module

        self.client = spotipy.Spotify(self.module.params.get("auth_token"))

    def album(self):
        album_dict = self.create_album_dict()
        results_dict = {'albums': []}

        try:
            for album in album_dict['album']:
                album_results = self.client.album(album)
                if album_results not in results_dict['albums']:
                    results_dict['albums'].append(album_results)

        except Exception as e:
            self.module.fail_json(msg="Error: Search for Album failed - " + str(e))

        results = results_dict
        return results

    def album_tracks(self):
        album_dict = self.create_album_dict()
        limit = self.module.params.get("limit")
        results_dict = {'tracks': []}

        try:
            for album in album_dict['album']:
                album_results = self.client.album_tracks(album_id=album,limit=limit)
                if album_results not in results_dict['tracks']:
                    results_dict['tracks'].append(album_results)
        except Exception as e:
            self.module.fail_json(msg="Error: Can't get album tracks for album: " + album_uri + " - " + str(e))

        results = results_dict
        return results

    def output_shortener(self, results_dict):
        if 'albums' in results_dict:
            if results_dict['albums']:
                output_shortener_dict = {'albums': []}
                for results in results_dict['albums']:
                    if 'uri' in results:
                        album_name = results['name']
                        album_uri = results['uri']

                    if 'artists' in results:
                        artists_list = []

                        for result in results['artists']:
                            artist_name = result['name']
                            artist_uri = result['uri']

                            artists_list.append({'name': artist_name, 'uri': artist_uri })

                    if 'tracks' in results:
                        if 'items' in results['tracks']:
                            tracks_list_dict = []

                            for result in results['tracks']['items']:
                                tracks_artists_list = []
                                track_name = result['name']
                                track_uri = result['uri']

                                for artists in result['artists']:
                                    track_artists_name = artists['name']
                                    track_artists_uri = artists['uri']

                                    tracks_artists_list.append({'name': track_artists_name, 'uri': track_artists_uri })

                                tracks_list_dict.append({'name': track_name, 'uri': track_uri, 'artists': tracks_artists_list})

                    output_shortener_dict['albums'].append({'name': album_name, 'uri': album_uri, 'artists': artists_list, 'tracks': tracks_list_dict})
        elif 'tracks' in results_dict:
            if results_dict['tracks']:
                output_shortener_dict = {'tracks': []}
                tracks_list_dict = []
                for album_tracks in results_dict['tracks']:
                    for items in album_tracks['items']:
                        tracks_artists_list = []
                        track_name = items['name']
                        track_uri = items['uri']

                        for artists in items['artists']:
                            track_artists_name = artists['name']
                            track_artists_uri = artists['uri']

                            tracks_artists_list.append({'name': track_artists_name, 'uri': track_artists_uri })

                        tracks_list_dict.append({'name': track_name, 'uri': track_uri, 'artists': tracks_artists_list})

                    output_shortener_dict.update({'tracks': tracks_list_dict})

        result = output_shortener_dict

        return result

    def create_album_dict(self):
        if self.module.params.get("album_uri"):
            album_dict = {'album': []}
            album_dict['album'].append(self.module.params.get("album_uri"))
        elif self.module.params.get("album_file"):
            album_file = self.module.params.get("album_file")
            album_dict = self.get_album_from_file(album_file)
        else:
            self.module.fail_json(msg="Error: No Album ID or file was given")

        return album_dict

    def get_album_from_file(self, album_file):
        album_dict = {'album': []}

        try:
            album_from_file = json.load(open(album_file))
        except Exception as e:
            self.module.fail_json(msg="Error: Can't load album file" + album_file + " - " + str(e))

        try:
            if 'albums' in album_from_file:
                if 'items' in album_from_file['albums']:
                    if album_from_file['albums']['items']:
                        for album in album_from_file['albums']['items']:
                            album_dict['album'].append(album['uri'])
                elif album_from_file['albums']:
                    for album in album_from_file['albums']:
                        album_dict['album'].append(album['uri'])
        except Exception as e:
            self.module.fail_json(msg="Error: Can't read dict in album file. - " + str(e))

        return album_dict

def main():
    argument_spec = {}
    argument_spec.update(dict(
        album_uri=dict(required=False, type='str'),
        album_file=dict(required=False, type='str'),
        auth_token=dict(required=True, type='str'),
        dest_file=dict(required=False, type='str'),
        limit=dict(required=False, default=50, type='int'),
        output_format=dict(required=False, default='long', choices=['short', 'long'], type='str'),
        state=dict(required=True, choices=['album', 'album_tracks'], type='str'),
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    output_format = module.params.get("output_format")
    state = module.params.get("state")

    search = SpotifySearch(module)

    if state == 'album':
        results = search.album()
    elif state == 'album_tracks':
        results = search.album_tracks()

    if output_format == 'short':
        results = search.output_shortener(results)

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
