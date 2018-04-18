#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1'}
DOCUMENTATION = '''
---
module: spotify_player
Ansible module for getting related artists for one artist
requirements:
  - python >= 2.6
  - spotipy >= 2.4.4
options:
   auth_token:
       description:
         - Authentication token for Spotify API
       required: True
       type: String
   state:
       description:
         - Player action to execute
       required: True
       type: String
       Choices: play, pause, next, previous, repeat, shuffle, volume
   volume_level:
       description:
          - Set volume level in percent
       type: int
   toggle_shuffle:
       description:
          - Set shuffle on or off
       type: String
       Choices: on, off
   repeat_mode:
       description:
          - Set shuffle on or off
       type: String
       Choices: track, context, off
'''

EXAMPLES = '''
- name: Execute play track
  spotify_player:
    auth_token=0123456789ABCDEFGHI
    state=play

- name: Execute next track
  spotify_player:
    auth_token=0123456789ABCDEFGHI
    state=next
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

    def volume(self):
        self.client.volume(self.module.params.get("volume_level"))

    def shuffle(self):
        if self.module.params.get("toggle_shuffle") == 'on':
            toggle = True
        else:
            toggle = False
        self.client.shuffle(toggle)

    def repeat(self):
        self.client.repeat(self.module.params.get("repeat_mode"))

def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        state=dict(required=True, choices=['play', 'pause', 'next', 'previous', 'repeat', 'shuffle', 'volume']),
        volume_level=dict(required=False, type='int'),
        toggle_shuffle=dict(required=False, choices=['on', 'off'], type='str'),
        repeat_mode=dict(required=False, choices=['track', 'context', 'off'], type='str'),

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
    elif module.params.get("state") == 'repeat':
        results = player.repeat()

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
