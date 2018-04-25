#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: spotify_search
short_description: Searching Spotify via Spotify API.
description:
    - "Ansible module to search in Spotify for Artists, Tracks, Albums, Artists & Track, Artists & Album or public Playlists via the Spotify API.

    Except for the states artists_and_albums and artists_and_tracks you can only define one of the options albums_name, artists_name, playlists_name or tracks_name.

    To search for artists_and_albums you need to define albums_name and artists_name.

    To Search for artists_and_tracks you need to define albums_name and tracks_name.

    The playlist search only allows you to search through public playlists. If you want to search through your personal playlists use the module spotify_user_playlists.

    The options dest_file, limit and output_format can be combined.

    Informations about the output format can be found here https://developer.spotify.com/web-api/search-item/."

version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)

options:

    albums_name:
        description:
          - Name of an album.
        type: String

    artists_name:
        description:
          - Name of an artist.
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

    playlists_name:
        description:
          - Name of an public playlist.
        type: String

    state:
        description:
          - Search to trigger.
        choices: ['artists', 'tracks', 'playlists', 'albums', 'artists_and_albums', 'artists_and_tracks']
        required: true
        type: String

    tracks_name:
        description:
          - Name of an track.
        type: String

requirements:
- python >= 2.7.10
- spotipy >= 2.4.4
'''

EXAMPLES = '''
- name: Search for artist Young the Giant and return maximum 10 search results
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: long
    state: artists
    artists_name: Young the Giant
    limit: 10
  register: artists_search_result

- name: Search for track containing Coug*
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    state: tracks
    tracks_name: Coug*

- name: Search for playlist Colombia with wildcard at the end and return maximum 20 search results
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: long
    state: playlists
    playlists_name: Colombia*
    limit: 20

- name: Search for Albums Arrival and return maximum 20 search results and save the output to a file
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    dest_file: search_result_albums.json
    output_format: long
    state: album
    albums_name: Arrival
    limit: 20

- name: Search for artists and album in combination
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: short
    state: artists_and_albums
    albums_name: Coexist
    artists_name: The xx
    limit: 20

- name: Search for artists and tracks in combination
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: short
    state: artists_and_albums
    tracks_name: Fiction
    artists_name: The xx
    limit: 20
'''
RETURN = '''
---
output:
  description: "returns a dict with the search result for artists and album in output_format short."
  returned: on success
  sample:
    changed: True
    result:
        albums:
        - album: Coexist
          artist: The xx
          uri: spotify:album:2cRMVS71c49Pf5SnIlJX3U
  type: dict

output:
  description: "returns a dict with the search result for playlists in output_format long."
  returned: on success
  sample:
    changed: True
    result:
        playlists:
          items:
          - name: Éxitos Colombia
            collaborative: false
            external_urls:
              spotify: https://open.spotify.com/user/spotify/playlist/37i9dQZF1DXbvPjXfc8G9S
            uri: spotify:user:spotify:playlist:37i9dQZF1DXbvPjXfc8G9S
            public:
            owner:
              display_name: Spotify
              external_urls:
                spotify: https://open.spotify.com/user/spotify
              uri: spotify:user:spotify
              href: https://api.spotify.com/v1/users/spotify
              type: user
              id: spotify
            tracks:
              total: 50
              href: https://api.spotify.com/v1/users/spotify/playlists/37i9dQZF1DXbvPjXfc8G9S/tracks
            href: https://api.spotify.com/v1/users/spotify/playlists/37i9dQZF1DXbvPjXfc8G9S
            snapshot_id: yBnt8hL8bFyoPN+8/MHVPC2CkSi5haDTCspx9821mGoNpNavK/gqauQlyoyl868VnUTf4ruylv0=
            images:
            - url: https://i.scdn.co/image/36d98030a7d4651025b385433a839d260e399b9f
              width: 300
              height: 300
            type: playlist
            id: 37i9dQZF1DXbvPjXfc8G9S
  type: dict

output:
  description: "returns a dict with the search result for an artists."
  returned: on success
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
  type: dict


output:
  description: "returns a dict with the search result for artists and tracks in output_format short."
  returned: on success
  sample:
    changed: True
    result:
        tracks:
        - track: Cough Syrup
          uri: spotify:track:1UqhkbzB1kuFwt2iy4h29Q
          artist: Young the Giant
        - track: Cough Syrup
          uri: spotify:track:4Tfe8Uu9faFdWRiZbpvpXd
          artist: Young the Giant
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

    def output_shortener(self, results):
        if self.module.params.get("state") == 'artists_and_albums':
            output_shortener_dict = {}
            if 'albums' in results:
                if results['albums']['items'][0]:
                    output_shortener_dict.update({'albums': []})
                    for result in results['albums']['items']:
                        album_name = result['name']
                        album_uri = result['uri']
                        for album_result in result['artists']:
                            artists_name = album_result['name']
                        output_shortener_dict['albums'].append({'artist': artists_name, 'album': album_name, 'uri': album_uri})
            elif 'artists' in results:
                if results['artists']['items'][0]:
                    output_shortener_dict.update({'artists': []})
                    for result in results['artists']['items']:
                        output_shortener_dict['artists'].append({'artist': result['name'], 'uri': result['uri']})

            result = output_shortener_dict
        elif self.module.params.get("state") == 'artists_and_tracks':
            output_shortener_dict = {}
            if 'tracks' in results:
                if results['tracks']['items'][0]:
                    output_shortener_dict.update({'tracks': []})
                    for result in results['tracks']['items']:
                        tracks_name = result['name']
                        tracks_uri = result['uri']
                        for tracks_result in result['artists']:
                            artists_name = tracks_result['name']
                        output_shortener_dict['tracks'].append({'artist': artists_name, 'track': tracks_name, 'uri': tracks_uri})
            elif 'artists' in results:
                if results['artists']['items'][0]:
                    output_shortener_dict.update({'artists': []})
                    for result in results['artists']['items']:
                        output_shortener_dict['artists'].append({'artist': result['name'], 'uri': result['uri']})

            result = output_shortener_dict
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
        albums_name=dict(required=False, type='str'),
        artists_name=dict(required=False, type='str'),
        auth_token=dict(required=True, type='str'),
        dest_file=dict(required=False, type='str'),
        limit=dict(required=False, default=10, type='int'),
        output_format=dict(required=False, default='long', choices=['short', 'long'], type='str'),
        playlists_name=dict(required=False, type='str'),
        state=dict(required=True, choices=['artists', 'tracks', 'playlists', 'albums', 'artists_and_albums', 'artists_and_tracks'], type='str'),
        tracks_name=dict(required=False, type='str')
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
        results = search.output_shortener(results)

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
