#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1'}
DOCUMENTATION = '''
---
module: spotify_user_info
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
   dest_file:
       description:
         - Destination file to save the output to
   output_format:
       description:
         - Output format
       Default: short
       type: String
       Choices: short, full
    username:
        description:
          - Username to get the playlist from
        required: True
        type: String
'''

EXAMPLES = '''
- name: Get user info for user muster and save to dest_file
  spotify_user_info:
    auth_token=0123456789ABCDEFGHI
    username: muster
    dest_file=artists.json
    output_format=short
'''


import sys
import os
import json
from ansible.module_utils.basic import *

try:
    import spotipy_connection
except ImportError as e:
    module.fail_json(msg="Error: Can't import required libraries - " + str(e))

class UserInfo:
    def __init__(self, module):
        self.module = module
        self.user_list = []

        self.client = spotipy_connection.client(self.module)

    def get(self):
        if self.module.params.get("username"):
            username = self.module.params.get("username")

        if username:
            try:
                result = self.client.user(username)
                return result
            except Exception as e:
              self.module.fail_json(msg="Error: Can't get user information - " + str(e))

        else:
            try:
                result = self.client.me()
                return result
            except Exception as e:
              self.module.fail_json(msg="Error: Can't get user information - " + str(e))

    def user_to_list(self, users_dict):
        self.user_list.append(users_dict['id'])
        return self.user_list

def main():
    argument_spec = {}
    argument_spec.update(dict(
        auth_token=dict(required=True, type='str'),
        username=dict(required=False, type='str'),
        output_format=dict(required=False, default='short', choices=['short', 'full'], type='str'),
        dest_file=dict(required=False, type='str')
    ))

    module = AnsibleModule(argument_spec=argument_spec)
    output_format = module.params.get("output_format")

    user = UserInfo(module)

    results = user.get()

    if output_format == 'short':
        results = user.user_to_list(results)

    if module.params.get("dest_file"):
        file = module.params.get("dest_file")
        with open(file, 'w') as f:
            json.dump(results, f)

    module.exit_json(changed=True, result=results)

if __name__ == '__main__':
    main()
