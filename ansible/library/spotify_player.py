#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: spotify_player
short_description: Ansible module for controlling your spotify.
description:
    - Ansible module for controlling your spotify. Play or pause a song, toggle repeat or shuffle, set volume, set transfer playback to a different device.

    To play a specific song define the option track_uri or track_file. track_file accept files created by the Ansible modules spotify_artists_top_tracks, spotify_user_info or spotify_search.

    To play songs from a specific artist define the option artist_uri or artist_file. artist_file accept files created by the Ansible modules spotify_related_artists, spotify_user_info or spotify_search.

    To play a specific playlist define the option playlist_uri or playlist_file. playlist_file accept files created by the Ansible modules spotify_user_playlists or spotify_search.

version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)

options:
    auth_token:
       description:
          - Spotify authentication token generated from the module spotify_auth and spotify_auth_create_user_token
       required: True
       type: String

    device_id:
       description:
         - Device ID you want to transfer the playback to.
       required: False
       type: String

    repeat_mode:
       description:
          - Set repeat mode.
       type: String
       choices: ['track', 'context', 'off']

    state:
       description:
         - Action to trigger.
       required: True
       type: String
       choices: ['play', 'pause', 'next', 'previous', 'repeat', 'shuffle', 'transfer_playback', 'volume']

    toggle_shuffle:
       description:
          - Set shuffle mode.
       type: String
       choices: ['on', 'off']

    volume_level:
       description:
          - Volume level in percent.
       type: int

    track_uri:
       description:
          - Define track uri to play.
       type: String

    track_file:
       description:
          - Define track file to play.
       type: String

    artist_uri:
       description:
          - Define artist uri to play tracks from.
       type: String

    artist_file:
       description:
          - Define artist file to play tracks from.
       type: String

    playlist_uri:
       description:
          - Define a playlist uri to play.
       type: String

    playlist_file:
       description:
          - Define a playlist file to play.
       type: String

    album_uri:
       description:
          - Define album uri to play tracks from.
       type: String

    album_file:
       description:
          - Define album file to play tracks from.
       type: String

- python >= 2.7.10
- spotipy >= 2.4.4
'''

EXAMPLES = '''
- name: Play track
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: play

- name: Play next track
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: next

- name: Play previous track
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    state: next

- name: Set repeat to repeat a single track
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    repeat_mode: track
    state: repeat

- name: Turn on shuffle
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    toggle_shuffle: on
    state: shuffle

- name: Transfer playback to a new device
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    device_id: 0123456789ABCDEFGHI
    state: transfer_playback

- name: Set playback volume on device to 80%
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    volume_level: 80
    state: volume
'''
RETURN = '''
---
output:
  description: "Returns null."
  returned: on success
  sample:
    changed: True
    result: null
  type: null
'''

import sys
import os
import json
from ansible.module_utils.basic import *

try:
    import spotipy
except ImportError as e:
    module.fail_json(msg="Error: Can't import required libraries - " + str(e))


class SpotifyPlayer:
    def __init__(self, module):
        self.module = module

        self.client = spotipy.Spotify(self.module.params.get("auth_token"))

    def play(self):
        context_uri = None
        track_uri = None
        device_id = None

        if self.module.params.get("track_file"):
            track_file = self.module.params.get("track_file")
            track_uri = self.get_tracks_from_file(track_file)
        if self.module.params.get("artist_file"):
            artist_file = self.module.params.get("artist_file")
            context_uri = self.get_uri_from_file(artist_file)
        if self.module.params.get("playlist_file"):
            playlist_file = self.module.params.get("playlist_file")
            context_uri = self.get_uri_from_file(playlist_file)
        if self.module.params.get("album_file"):
            album_file = self.module.params.get("album_file")
            context_uri = self.get_uri_from_file(album_file)
        if self.module.params.get("artist_uri"):
            artist_uri = self.module.params.get("artist_uri")
            context_uri = artist_uri
        if self.module.params.get("track_uri"):
            track_uri = self.module.params.get("track_uri")
            track_uri = [track_uri]
        if self.module.params.get("playlist_uri"):
            playlist_uri = self.module.params.get("playlist_uri")
            context_uri = playlist_uri
        if self.module.params.get("device_id"):
            device_id = self.module.params.get("device_id")

        self.client.start_playback(device_id=device_id, context_uri=context_uri, uris=track_uri)

    def pause(self):
        self.client.pause_playback()

    def next(self):
        self.client.next_track()

    def previous(self):
        self.client.previous_track()

    def repeat(self):
        self.client.repeat(self.module.params.get("repeat_mode"))

    def shuffle(self):
        if self.module.params.get("toggle_shuffle") == 'on':
            toggle = True
        else:
            toggle = False

        self.client.shuffle(toggle)

    def transfer_playback(self):
        if self.module.params.get("device_id"):
            device_id = self.module.params.get("device_id")
        else:
            module.fail_json(msg="Error: Can't transfer song to device. No Device ID was given")
        self.client.transfer_playback(device_id)

    def volume(self):
        self.client.volume(self.module.params.get("volume_level"))

    def get_tracks_from_file(self, track_file):
        tracks_list = []

        try:
            track_from_file = json.load(open(track_file))
        except Exception as e:
            self.module.fail_json(msg="Error: Can't load track file" + track_file + " - " + str(e))

        try:
            if 'tracks' in track_from_file:
                if track_from_file['tracks']:
                    for track in track_from_file['tracks']:
                        tracks_list.append(track['uri'])
            elif 'items' in track_from_file:
                if track_from_file['items']:
                    for track in track_from_file['items']:
                        tracks_list.append(track['uri'])
            elif 'type' in track_from_file:
                if track_from_file['type'] == 'track':
                        tracks_list.append(track_from_file['uri'])
        except Exception as e:
            self.module.fail_json(msg="Error: Can't read dict in tracks file. - " + str(e))

        return tracks_list

    def get_uri_from_file(self, uri_file):
        try:
            uri_from_file = json.load(open(uri_file))
        except Exception as e:
            self.module.fail_json(msg="Error: Can't load playlist file" + uri_file + " - " + str(e))

        if 'playlists' in uri_from_file:
            if 'items' in uri_from_file['playlists']:
                if uri_from_file['playlists']['items']:
                    uri = uri_from_file['playlists']['items'][0]['uri']
            elif uri_from_file['playlists']:
                uri = uri_from_file['playlists'][0]['uri']
        elif 'artists' in uri_from_file:
            if 'items' in uri_from_file['artists']:
                if uri_from_file['artists']['items']:
                    uri = uri_from_file['artists']['items'][0]['uri']
            elif uri_from_file['artists']:
                uri = uri_from_file['artists'][0]['uri']
        elif 'albums' in uri_from_file:
            if 'items' in uri_from_file['albums']:
                if uri_from_file['albums']['items']:
                    uri = uri_from_file['albums']['items'][0]['uri']
            elif uri_from_file['albums']:
                uri = uri_from_file['albums'][0]['uri']
        elif 'items' in uri_from_file:
            if uri_from_file['items']:
                uri = uri_from_file['items'][0]['uri']
        elif 'uri' in uri_from_file:
            uri = uri_from_file['uri']
        else:
            self.module.fail_json(msg="Error: Can't read dict in file. - " + str(e))

        return uri

def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        device_id=dict(required=False, type='str'),
        repeat_mode=dict(required=False, choices=['track', 'context', 'off'], type='str'),
        state=dict(required=True, choices=['play', 'pause', 'next', 'previous', 'repeat', 'shuffle', 'transfer_playback', 'volume']),
        track_file=dict(required=False, type='str'),
        album_file=dict(required=False, type='str'),
        artist_file=dict(required=False, type='str'),
        playlist_file=dict(required=False, type='str'),
        album_uri=dict(required=False, type='str'),
        artist_uri=dict(required=False, type='str'),
        track_uri=dict(required=False, type='str'),
        playlist_uri=dict(required=False, type='str'),
        toggle_shuffle=dict(required=False, choices=['on', 'off'], type='str'),
        volume_level=dict(required=False, type='int')
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    output_format = module.params.get("output_format")

    player = SpotifyPlayer(module)

    if module.params.get("state") == 'play':
        results = player.play()
    elif module.params.get("state") == 'pause':
        results = player.pause()
    elif module.params.get("state") == 'next':
        results = player.next()
    elif module.params.get("state") == 'previous':
        results = player.previous()
    elif module.params.get("state") == 'volume':
        results = player.volume()
    elif module.params.get("state") == 'shuffle':
        results = player.shuffle()
    elif module.params.get("state") == 'transfer_playback':
        results = player.transfer_playback()
    elif module.params.get("state") == 'repeat':
        results = player.repeat()

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
