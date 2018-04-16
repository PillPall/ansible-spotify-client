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
   state:
       description:
         - What to search for
       required: True
       Choices: artists, tracks
       type: String
   artists_name:
       description:
         - Artists name to search for
       type: String
   tracks_name:
       description:
         - Track name to search for
       type: String
   limit:
       description:
         - Limit search result to
       default: 10
       type: String
'''

EXAMPLES = '''
- name: Search for artist Young the Giant and return maximum 50 search results
  spotify_search:
    auth_token=0123456789ABCDEFGHI
    output_format=full
    state=artists
    artists_name=Young the Giant
    limit=50
  register: artists_search_result

- name: Search for track cough syrup and return maximum 20 search results
  spotify_search:
    auth_token=0123456789ABCDEFGHI
    dest_file=search_result_tracks.json
    output_format=full
    state=tracks
    tracks_name=cough syrup
    limit=20

- name: Search for playlist Colombia with wildcard at the end and return maximum 20 search results
  spotify_search:
    auth_token=0123456789ABCDEFGHI
    output_format=full
    state=playlists
    playlists_name=Colombia*
    limit=20

- name: Search for Albums Arrival and return maximum 20 search results
  spotify_search:
    auth_token=0123456789ABCDEFGHI
    dest_file=search_result_albums.json
    output_format=full
    state=tracks
    albums_name=Arrival
    limit=20

- name: Search for Artists starts with Ab* and all Albums Start with Arr and return maximum 20 search results
  spotify_search:
    auth_token=0123456789ABCDEFGHI
    dest_file=search_result_albums.json
    output_format=full
    state=tracks
    artists_name=Ab*
    albums_name=Arr*
    limit=20
'''


import sys
import os
import json
from ansible.module_utils.basic import *

try:
    import spotipy_connection
except ImportError as e:
    module.fail_json(msg="Error: Can't import required libraries - " + str(e))

class SpotifySearch:
    def __init__(self, module):
        self.module = module

        self.client = spotipy_connection.client(self.module)

    def artists(self):
        artists_name = self.module.params.get("artists_name")
        limit = self.module.params.get("limit")

        try:
            results = spotipy_connection.sp_search(self.client, q='artist:' + artists_name, limit=limit, type='artist')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for artists: " + artists_name + " failed - " + str(e))

        return results

    def tracks(self):
        tracks_name = self.module.params.get("tracks_name")
        limit = self.module.params.get("limit")

        try:
            results = spotipy_connection.sp_search(self.client, q='track:' + tracks_name, limit=limit, type='track')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for Track: " + tracks_name + " failed - " + str(e))

        return results

    def playlists(self):
        playlists_name = self.module.params.get("playlists_name")
        limit = self.module.params.get("limit")

        try:
            results = spotipy_connection.sp_search(self.client, q=playlists_name, limit=limit, type='playlist')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for Playlist: " + playlists_name + " failed - " + str(e))

        return results

    def albums(self):
        albums_name = self.module.params.get("albums_name")
        limit = self.module.params.get("limit")

        try:
            results = spotipy_connection.sp_search(self.client, q='album:' + albums_name, limit=limit, type='album')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for Album: " + albums_name + " failed - " + str(e))

        return results

    def artists_and_albums(self):
        artists_name = self.module.params.get("artists_name")
        albums_name = self.module.params.get("albums_name")
        limit = self.module.params.get("limit")

        try:
            results = spotipy_connection.sp_search(self.client, q=artists_name + ' ' + albums_name, limit=limit, type='artists_and_album')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for artists: " + artists_name + "and Album: " + albums_name + " failed - " + str(e))

        return results

    def artists_and_tracks(self):
        artists_name = self.module.params.get("artists_name")
        tracks_name = self.module.params.get("tracks_name")
        limit = self.module.params.get("limit")

        try:
            results = spotipy_connection.sp_search(self.client, q=artists_name + ' ' + tracks_name, limit=limit, type='artists_and_tracks')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for artists: " + artists_name + "and Track: " + tracks_name + " failed - " + str(e))

        return results

    def search_results_to_list(self, results):
        if self.module.params.get("state") == 'artists_and_albums':
            search_result_dict = {}
            if  results['albums']['items'][0]['name']:
                search_result_dict.update({'albums': [{}]})
                for result in results['albums']['items']:
                    album_name = result['name']
                    for album_result in result['artists']:
                        artists_name = album_result['name']
                    search_result_dict['albums'].append({'Artists': artists_name, 'Album': album_name})
            elif  results['artists']['items'][0]['name']:
                search_result_dict.update({'artists': []})
                for result in results['artists']['items']:
                  search_result_dict['artists'].append([result['name']])
            else:
                search_result_dict = {}
            result = search_result_dict
        elif self.module.params.get("state") == 'artists_and_tracks':
            search_result_dict = {}
            if  results['tracks']['items'][0]['name']:
                search_result_dict.update({'tracks': [{}]})
                for result in results['tracks']['items']:
                    tracks_name = result['name']
                    for tracks_result in result['artists']:
                        artists_name = tracks_result['name']
                    search_result_dict['tracks'].append({'Artists': artists_name, 'Track': tracks_name})
            elif  results['artists']['items'][0]['name']:
                search_result_dict.update({'artists': []})
                for result in results['artists']['items']:
                  search_result_dict['artists'].append([result['name']])
            else:
                search_result_dict = {}
            result = search_result_dict
        else:
            search_result_list = []
            for result in results[self.module.params.get("state")]['items']:
              search_result_list.append(result['name'])
            result = search_result_list

        return result

def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        output_format=dict(required=False, default='short', choices=['short', 'full'], type='str'),
        dest_file=dict(required=False, type='str'),
        state=dict(required=True, choices=['artists', 'tracks', 'playlists', 'albums', 'artists_and_albums', 'artists_and_tracks'], type='str'),
        artists_name=dict(required=False, type='str'),
        albums_name=dict(required=False, type='str'),
        tracks_name=dict(required=False, type='str'),
        playlists_name=dict(required=False, type='str'),
        limit=dict(required=False, default=10, type='int')
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    output_format = module.params.get("output_format")
    state = module.params.get("state")

    search = SpotifySearch(module)

    if state == 'artists':
        search_results = search.artists()
    elif state == 'tracks':
        search_results = search.tracks()
    elif state == 'playlists':
        search_results = search.playlists()
    elif state == 'albums':
        search_results = search.albums()
    elif state == 'artists_and_albums':
        search_results = search.artists_and_albums()
    elif state == 'artists_and_tracks':
        search_results = search.artists_and_tracks()

    if output_format == 'short':
        results = search.search_results_to_list(search_results)
    else:
        results = search_results

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
