#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: spotify_update_playlists
short_description: Update one or more user playlists.
description:
    - "Ansible module to add or remove tracks to/from a user playlist. Tracks and playlists can be provided via a JSON File.
    Visit https://developer.spotify.com/documentation/web-api/reference/object-model/ for more informations."
version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)

options:
    auth_token:
        description:
          - Spotify API authentication token
        required: True
        type: String

    dest_file:
        description:
          - Path to file to save the search result.
        type: String

    playlist_id:
        description:
          - Playlist ID or URI to update.
        type: String

    playlist_file:
        description:
          - JSON File containing a dict of Playlist ID or URI to update. Fore more information about the JSON structure
            visit https://beta.developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/.
        type: String

    state:
        description:
          - Add or remove tracks from playlist
        choices: ['add', 'remove']
        required: True
        type: String

    track_id:
        description:
          - Track ID or URI to update.
        type: String

    track_file:
        description:
          - JSON File containing a dict of Track IDs or URIs to update. Fore more information about the JSON structure
            visit https://beta.developer.spotify.com/documentation/web-api/reference/artists/get-artists-top-tracks/.
        type: String

    username:
        description:
          - Username to update the playlist for
        required: True
        type: String

requirements:
- python >= 2.7.10
- spotipy >= 2.4.4
'''


EXAMPLES = '''

- name: Add songs to playlist from playlist_file with defined track uri
  spotify_update_playlists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    username: "USER"
    state: "add"
    playlist_file: "{{ playbook_dir }}/files/create_playlist_user.json"
    track_id: spotify:track:1YZDkJOFT8xlAXDi8lneb3

- name: Add songs to playlist with playlist_id with defined track_file and dest_file
  spotify_update_playlists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    username: "USER"
    state: "add"
    playlist_id: spotify:user:USER:playlist:BCASDJLASDKV12345
    track_file: "{{ playbook_dir }}/files/tracks.json"
    dest_file: "{{ dest_file }}"

- name: Remove songs from playlist with playlist_file and defined track_file
  spotify_update_playlists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    username: "USER"
    state: "remove"
    playlist_file: "{{ playbook_dir }}/files/create_playlist_user.json"
    track_file: "{{ playbook_dir }}/files/tracks.json"

- name: Remove songs from playlist with playlist_id and defined track_id
  spotify_update_playlists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    username: "USER"
    state: "remove"
    playlist_id: spotify:user:USER:playlist:BCASDJLASDKV12345
    track_id: spotify:track:1YZDkJOFT8xlAXDi8lneb3
    dest_file: "{{ playbook_dir }}/files/update_playlist_user.json"

- name: Example of how to use spotify_artists_top_tracks module to update a playlist
  spotify_artists_top_tracks:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_name: "Young the Giant"
    dest_file: "{{ playbook_dir }}/files/tracks.json"

- name: Add songs to playlist
  spotify_update_playlists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    username: "USER"
    state: "add"
    playlist_id: spotify:user:USER:playlist:BCASDJLASDKV12345
    track_file: "{{ playbook_dir }}/files/tracks.json"
'''
RETURN = '''
---
output:
  description: "returns a dict with the snapshot_ids of the updated playlists"
  returned: on success
  sample:
    changed: True
    result:
        snapshot_id: 4HJAHdr2BypGxe/esgasdfihIMcv4luhnZlAhGXL295BefUSisFtRjl0D8CxGqaVrY
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

class UpdatePlaylist:
    def __init__(self, module):
        self.module = module
        self.playlists_list = []

        self.client = spotipy.Spotify(self.module.params.get("auth_token"))


    def add(self):
        method_to_call = self.client.user_playlist_add_tracks

        results = self.update_playlist_looper(method_to_call)

        return results

    def remove(self):
        method_to_call = self.client.user_playlist_remove_all_occurrences_of_tracks

        results = self.update_playlist_looper(method_to_call)

        return results

    def update_playlist_looper(self, method_caller):
        username = self.module.params.get("username")
        tracks_dict = self.create_tracks_dict()
        playlist_dict = self.create_playlist_dict()

        results = {'result': []}
        track_dict_list_length = len(tracks_dict['tracks'])
        i = 0
        ii = 49
        done = False

        for playlist in playlist_dict['playlists']:
            while not done:
                if track_dict_list_length == 1:
                   iii = track_dict_list_length - 1
                   track = [tracks_dict['tracks'][iii]]
                   try:
                       result = method_caller(username, playlist, track)
                       results['result'].append(result)
                   except Exception as e:
                       self.module.fail_json(msg="Error: Can't update playlist  - " + str(e))
                   done = True
                elif ii == track_dict_list_length:
                    iii = track_dict_list_length - 1
                    track = tracks_dict['tracks'][i:iii]
                    try:
                        result = method_caller(username, playlist, track)
                        results['result'].append(result)
                    except Exception as e:
                        self.module.fail_json(msg="Error: Can't update playlist  - " + str(e))
                    done = True
                elif ii > track_dict_list_length:
                    iii = track_dict_list_length - 1
                    track = tracks_dict['tracks'][i:iii]
                    try:
                        result = method_caller(username, playlist, track)
                        results['result'].append(result)
                    except Exception as e:
                        self.module.fail_json(msg="Error: Can't update playlist  - " + str(e))
                    done = True
                while ii < track_dict_list_length:
                     track = tracks_dict['tracks'][i:ii]
                     try:
                         result = method_caller(username, playlist, track)
                         results['result'].append(result)
                     except Exception as e:
                       self.module.fail_json(msg="Error: Can't update playlist  - " + str(e))
                     i = i + 49
                     ii = ii + 49
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

    def create_playlist_dict(self):
        if self.module.params.get("playlist_id"):
            playlists_dict = {'playlists': []}
            playlists_dict['playlists'].append(self.module.params.get("playlist_id"))

        elif self.module.params.get("playlist_file"):
            playlist_file = self.module.params.get("playlist_file")
            playlists_dict = self.get_playlist_from_file(playlist_file)
        else:
            self.module.fail_json(msg="Error: No Playlist ID or file was given")

        return playlists_dict

    def get_playlist_from_file(self, playlist_file):
        playlists_dict = {'playlists': []}

        try:
            playlists_from_file = json.load(open(playlist_file))
        except Exception as e:
          self.module.fail_json(msg="Error: Can't load playlist file" + playlist_file + " - " + str(e))

        if playlists_from_file.has_key('playlists'):
            if ['playlists'][0]:
                for playlist in playlists_from_file['playlists']:
                    playlists_dict['playlists'].append(playlist['uri'])
        elif playlists_from_file.has_key('items'):
            if playlists_from_file['items'][0]:
                for playlist in playlists_from_file['items']:
                    playlists_dict['playlists'].append(playlist['uri'])
        elif playlists_from_file.has_key('type'):
            if playlists_from_file['type'] == 'playlist':
                    playlists_dict['playlists'].append(playlists_from_file['uri'])
        else:
            self.module.fail_json(msg="Error: Can't read dict in artists file. See https://developer.spotify.com/web-api/get-related-artists/ for a correct dict structure." )

        return playlists_dict

    def get_tracks_from_file(self, track_file):
        tracks_dict = {'tracks': []}

        try:
            track_from_file = json.load(open(track_file))
        except Exception as e:
          self.module.fail_json(msg="Error: Can't load track file" + track_file + " - " + str(e))

        if track_from_file.has_key('tracks'):
            if track_from_file['tracks'][0]:
                for track in track_from_file['tracks']:
                    tracks_dict['tracks'].append(track['uri'])
        elif track_from_file.has_key('items'):
            if track_from_file['items'][0]:
                for track in track_from_file['items']:
                    tracks_dict['tracks'].append(track['uri'])
        elif track_from_file.has_key('type'):
            if track_from_file['type'] == 'track':
                    tracks_dict['tracks'].append(track_from_file['uri'])
        else:
            self.module.fail_json(msg="Error: Can't read dict in artists file. See https://developer.spotify.com/web-api/get-related-artists/ for a correct dict structure." )

        return tracks_dict

def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        dest_file=dict(required=False, type='str'),
        playlist_id=dict(required=False, type='str'),
        playlist_file=dict(required=False, type='str'),
        state=dict(required=True, choices=['add', 'remove'], type='str'),
        track_id=dict(required=False, type='str'),
        track_file=dict(required=False, type='str'),
        username=dict(required=True, type='str')
    ))
    module = AnsibleModule(argument_spec=argument_spec)
    output_format = module.params.get("output_format")
    state = module.params.get("state")

    update_playlist = UpdatePlaylist(module)

    if state == 'add':
        results = update_playlist.add()
    elif state == 'remove':
        results = update_playlist.remove()

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
