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
    - "Ansible module for controlling your spotify. Play or pause a song, toggle shuffle on/off or set the volume."

version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)

options:
    auth_token:
       description:
         - Authentication token for Spotify API
       required: True
       type: String

    device_Id:
       description:
         - Device ID to transfer a User's Playback
       required: True
       type: String

    repeat_mode:
       description:
          - Set shuffle on or off
       type: String
       choices: ['track', 'context', 'off']

    state:
       description:
         - Player action to execute
       required: True
       type: String
       choices: ['play', 'pause', 'next', 'previous', 'repeat', 'shuffle', 'volume']

    toggle_shuffle:
       description:
          - Set shuffle on or off
       type: String
       choices: ['on', 'off']

    volume_level:
       description:
          - Set volume level in percent
       type: int

requirements:
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

- name: Transfer playback to a new device
  spotify_player:
    auth_token: 0123456789ABCDEFGHI
    device_id: 0123456789ABCDEFGHI
    state: transfer_playback
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
        self.client.start_playback()

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
def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        device_id=dict(required=False, type='str'),
        repeat_mode=dict(required=False, choices=['track', 'context', 'off'], type='str'),
        state=dict(required=True, choices=['play', 'pause', 'next', 'previous', 'repeat', 'shuffle', 'transfer_playback', 'volume']),
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
