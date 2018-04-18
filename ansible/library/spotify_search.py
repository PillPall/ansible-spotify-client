#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: sp_search
short_description: Searching Spotify via Spotify API.
description:
    - "Ansible module to search in Spotify for Artists, Tracks, Albums, Artists & Track, Artists & Album or public Playlists via the Spotify API."

version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)

options:
    auth_token:
        description:
          - Spotify API authentication token
        required: false
        Type: String

    output_format:
        description:
          - Control Ansible output.
        required: false
        default: full
        choices: ['short', 'full']
        Type: String

    dest_file:
        description:
          - Path to file to save the search result.
        required: false
        Type: String

    state:
        description:
          - Parameter to define what to search for.
        choices: ['artists', 'tracks', 'playlists', 'albums', 'artists_and_albums', 'artists_and_tracks']
        required: true
        Type: String

    limit:
        description:
          - Limit the search result  to X results.
        required: false
        default: 10
        Type: Integer

    artists_name:
        description:
          - Artists name to search for.
        required: false
        Type: String

    albums_name:
        description:
          - Album name to search for.
        required: false
        Type: String

    tracks_name:
        description:
          - Track name to search for.
        required: false
        Type: String

    playlists_name:
        description:
          - Playlist name to search for.
        required: false
        Type: String

requirements:
- python >= 2.7.10
- spotipy >= 2.4.4
'''


EXAMPLES = '''
- name: Search for artist Young the Giant and return maximum 10 search results
  spotify_search:
    auth_token=0123456789ABCDEFGHI
    output_format=full
    state=artists
    artists_name=Young the Giant
    limit=10
  register: artists_search_result

- name: Search for artists start with Young maximum 50 search results
  spotify_search:
    auth_token=0123456789ABCDEFGHI
    output_format=full
    state=artists
    artists_name=Young
    limit=50
  register: artists_search_result

- name: Search for track cough syrup, return maximum 20 search results and save it to search_result_tracks.json
  spotify_search:
    auth_token=0123456789ABCDEFGHI
    dest_file=search_result_tracks.json
    output_format=short
    state=tracks
    tracks_name=cough syrup
    limit=20

- name: Search for track containing Coug*, return maximum 20 search results and save it to search_result_tracks.json
  spotify_search:
    auth_token=0123456789ABCDEFGHI
    dest_file=search_result_tracks.json
    output_format=short
    state=tracks
    tracks_name=Coug*
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
RETURN = '''
---
output:
  description: "returns a dict with the search result.
  More information about the search result output can be found here https://developer.spotify.com/web-api/search-item/"
  returned: always
  sample:
    changed: True
    result:
        artists:
          href: https://api.spotify.com/v1/search?query=artist%3AYoung+the+Giant&type=artist&offset=0&limit=1
          items:
          - external_urls:
              spotify: https://open.spotify.com/artist/4j56EQDQu5XnL7R3E9iFJT
            followers:
              href:
              total: 780072
            genres:
            - indie pop
            - indie rock
            - indietronica
            - la indie
            - modern rock
            - shimmer pop
            - stomp and holler
            href: https://api.spotify.com/v1/artists/4j56EQDQu5XnL7R3E9iFJT
            id: 4j56EQDQu5XnL7R3E9iFJT
            images:
            - height: 640
              url: https://i.scdn.co/image/04ec224d5a225ef58b300d9942af24b7e2ad3320
              width: 640
            - height: 320
              url: https://i.scdn.co/image/f4dbc17572a1b8010ffdea9b6d43acec2d92b004
              width: 320
            - height: 160
              url: https://i.scdn.co/image/5eb442e4c439d9e7799a1a26fe67fad075ad80fa
              width: 160
            name: Young the Giant
            popularity: 68
            type: artist
            uri: spotify:artist:4j56EQDQu5XnL7R3E9iFJT
          limit: 1
          next:
          offset: 0
          previous:
          total: 1
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

    def artists(self):
        artists_name = self.module.params.get("artists_name")
        limit = self.module.params.get("limit")

        try:
            results = self.sp_search(q='artist:' + artists_name, limit=limit, type='artist')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for artists: " + artists_name + " failed - " + str(e))

        return results

    def tracks(self):
        tracks_name = self.module.params.get("tracks_name")
        limit = self.module.params.get("limit")

        try:
            results = self.sp_search(q='track:' + tracks_name, limit=limit, type='track')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for Track: " + tracks_name + " failed - " + str(e))

        return results

    def playlists(self):
        playlists_name = self.module.params.get("playlists_name")
        limit = self.module.params.get("limit")

        try:
            results = self.sp_search(q=playlists_name, limit=limit, type='playlist')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for Playlist: " + playlists_name + " failed - " + str(e))

        return results

    def albums(self):
        albums_name = self.module.params.get("albums_name")
        limit = self.module.params.get("limit")

        try:
            results = self.sp_search(q='album:' + albums_name, limit=limit, type='album')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for Album: " + albums_name + " failed - " + str(e))

        return results

    def artists_and_albums(self):
        artists_name = self.module.params.get("artists_name")
        albums_name = self.module.params.get("albums_name")
        limit = self.module.params.get("limit")

        try:
            results = self.sp_search(q=artists_name + ' ' + albums_name, limit=limit, type='artists_and_album')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for artists: " + artists_name + "and Album: " + albums_name + " failed - " + str(e))

        return results

    def artists_and_tracks(self):
        artists_name = self.module.params.get("artists_name")
        tracks_name = self.module.params.get("tracks_name")
        limit = self.module.params.get("limit")

        try:
            results = self.sp_search(q=artists_name + ' ' + tracks_name, limit=limit, type='artists_and_tracks')
        except Exception as e:
          self.module.fail_json(msg="Error: Search for artists: " + artists_name + "and Track: " + tracks_name + " failed - " + str(e))

        return results

    def search_results_to_list(self, results):
        if self.module.params.get("state") == 'artists_and_albums':
            search_result_dict = {}
            if  results['albums']['items'][0]['name']:
                search_result_dict.update({'albums': []})
                for result in results['albums']['items']:
                    album_name = result['name']
                    album_uri = result['uri']
                    for album_result in result['artists']:
                        artists_name = album_result['name']
                    search_result_dict['albums'].append({'artist': artists_name, 'album': album_name, 'uri': album_uri})
            elif results['artists']['items'][0]['name']:
                search_result_dict.update({'artists': []})
                for result in results['artists']['items']:
                  search_result_dict['artists'].append({'artist': result['name'], 'uri': result['uri']})
            else:
                search_result_dict = {}
            result = search_result_dict
        elif self.module.params.get("state") == 'artists_and_tracks':
            search_result_dict = {}
            if  results['tracks']['items'][0]['name']:
                search_result_dict.update({'tracks': []})
                for result in results['tracks']['items']:
                    tracks_name = result['name']
                    tracks_uri = result['uri']
                    for tracks_result in result['artists']:
                        artists_name = tracks_result['name']
                    search_result_dict['tracks'].append({'artist': artists_name, 'track': tracks_name, 'uri': tracks_uri})
            elif results['artists']['items'][0]['name']:
                search_result_dict.update({'artists': []})
                for result in results['artists']['items']:
                  search_result_dict['artists'].append({'artist': result['name'], 'uri': result['uri']})
            else:
                search_result_dict = { }
            result = search_result_dict
        else:
            search_result_list = {self.module.params.get("state"): []}
            for result in results[self.module.params.get("state")]['items']:
              search_result_list[self.module.params.get("state")].append({self.module.params.get("state"): result['name'], 'uri': result['uri']})
            result = search_result_list

        return result

    def sp_search(self, q, limit=10, offset=0, type='artist', market=None):
        if type is 'artist':
            return self.client.search(q=q, limit=limit, offset=offset, type=type, market=market)
        elif type is 'album':
            return self.client.search(q=q, limit=limit, offset=offset, type=type, market=market)
        elif type is 'playlist':
            return self.client.search(q=q, limit=limit, offset=offset, type=type, market=market)
        elif type is 'track':
            return self.client.search(q=q, limit=limit, offset=offset, type=type, market=market)
        elif type is 'artists_and_album':
            return self.client.search(q=q, limit=limit, offset=offset, type='artist,album', market=market)
        elif type is 'artists_and_tracks':
            return self.client.search(q=q, limit=limit, offset=offset, type='artist,track', market=market)

def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        output_format=dict(required=False, default='full', choices=['short', 'full'], type='str'),
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
        results = search.artists()
    elif state == 'tracks':
        results = search.tracks()
    elif state == 'playlists':
        results = search.playlists()
    elif state == 'albums':
        results = search.albums()
    elif state == 'artists_and_albums':
        results = search.artists_and_albums()
    elif state == 'artists_and_tracks':
        results = search.artists_and_tracks()

    if output_format == 'short':
        results = search.search_results_to_list(results)

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
