#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1'}
DOCUMENTATION = '''
---
module: spotipy_related_artists
Ansible module for getting related artists for one artist
requirements:
  - python >= 2.6
options:
    client_id:
        description:
          - Spotify API Client ID
        required: false

'''

EXAMPLES = '''
- name: Get top ten tracks for an artist in australia and save it to file
  spotipy_authentication_create_user_token:
    client_id=0123456789ABCDEFGHI
    client_secret=JKLMNOPQRSTUVWXZY
    artist_name=young the giant
    country=au
    dest_file=artists.json
    output_format=short

- name: Get top ten tracks for an artist in germany
  spotipy_authentication_create_user_token:
    config_file: "{{playbook_dir}}/../inventory/group_vars/all.yaml"
    artist_name=young the giant
    country=de
    output_format=long
  register: results

'''


import sys
import os
import json
from ansible.module_utils.basic import *

try:
    import spotipy.oauth2 as oauth2
    import spotipy_connection
except ImportError as e:
    module.fail_json(msg="Error: Can't import required libraries - " + str(e))

class UserTokenCreation:
    def __init__(self, module):
        self.module = module
        self.config = spotipy_connection.create_config(self.module)
        self.token_dict = {}

    def create_user_token(self):
        conf = self.config
        user_code = self.module.params.get("user_code")
        username = self.module.params.get("username")
        cache_path = "/tmp/.cache-" + username
        try:
            sp_oauth = oauth2.SpotifyOAuth(cache_path=cache_path, **conf)
            token_info = sp_oauth.get_access_token(user_code)
            token = token_info['access_token']
            self.token_dict.update({'client': 'user'})
            self.token_dict.update({'token': token})
        except Exception as e:
            self.module.fail_json(msg="Error: Can't get user token - " + str(e))

        return self.token_dict

def main():
    argument_spec = {}
    argument_spec.update(dict(
            user_code=dict(required=True, type='str' ),
            username=dict(required=True, type='str'),
            client_id=dict(required=False, type='str' ),
            client_secret=dict(required=False, type='str'),
            config_file=dict(required=False, type='str'),
            redirect_uri=dict(defualt='https://example.com/callback/',required=False, type='str'),
            scope=dict(defualt='',required=False, type='str')
            ))

    module = AnsibleModule(argument_spec=argument_spec)

    sp_user_token = UserTokenCreation(module)
    results = sp_user_token.create_user_token()

    module.exit_json(changed=True, results=results)

if __name__ == '__main__':
    main()
