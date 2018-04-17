#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1'}
DOCUMENTATION = '''
---
module: sp_auth
Ansible module for authentication to the Spotify API. This module will response with an
requirements:
  - python >= 2.6
  - spotipy >= 2.4.4
options:
    client_id:
        description:
          - Spotify API Client ID
        required: false
        Type: String
    client_secret:
        description:
          - Spotify API Client Secret Key
        required: false
        Type: String
    config_file:
        description:
          - Configuration file containing Spotify API Authentication parameters
        required: false
        Type: String
    redirect_uri:
        description:
          - Redirect URL, required for user authentication
        required: false
        Type: String
    scope:
        description:
          - Scope, required for User authentication. For avaiable scopes see here:
            https://developer.spotify.com/web-api/using-scopes/
        required: false
        Type: String
    username:
        description:
          - Spotify Username, required for user authentication
        required: false
        Type: String
'''

EXAMPLES = '''
- name: Provide client ID and client secret for Public authentication token
  sp_auth:
    client_id=0123456789ABCDEFGHI
    client_secret=JKLMNOPQRSTUVWXZY

- name: Provide all options for user authentication token
  sp_auth:
    username: spotify_user
    client_id=0123456789ABCDEFGHI
    client_secret=JKLMNOPQRSTUVWXZY
    redirect_uri=https://example.com/callback/
    scope=user-top-read,playlist-read-private

- name: Provide all configuration parameters via config file
  sp_auth:
    username: spotify_user
    config_file="{{ inventory_dir}}/user.yaml"
'''


import sys
import yaml
import os
import json
from ansible.module_utils.basic import *

try:
    import spotipy.oauth2 as oauth2
    import spotipy_connection
except ImportError as e:
    module.fail_json(msg="Error: Can't import required libraries - " + str(e))

class SpotifyAuthentication:
    def __init__(self, module):
        self.module = module
        self.config = spotipy_connection.create_config(self.module)
        self.token_dict = {}

    def public_client(self):
        conf = self.config
        credentials = oauth2.SpotifyClientCredentials(**conf)
        try:
            token = credentials.get_access_token()
            self.token_dict.update({'client': 'public'})
            self.token_dict.update({'token': token})
            return self.token_dict

        except Exception as e:
            self.module.fail_json(msg="Error: Can't finish authentication - " + str(e))

    def user_client(self):
        conf = self.config
        username = self.module.params.get("username")
        cache_path = "/tmp/.cache-" + username
        sp_oauth = oauth2.SpotifyOAuth(cache_path=cache_path, **conf)
        token_info = sp_oauth.get_cached_token()


        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            try:
                import webbrowser
                webbrowser.open(auth_url)

            except Exception as e:
                self.module.fail_json(msg="Error: Can't open browser for authentication - " + str(e))

        if token_info:
            token = token_info['access_token']
            self.token_dict.update({'cached': 1})
            self.token_dict.update({'client': 'user'})
            self.token_dict.update({'token': token})
        else:
            self.token_dict.update({'cached': 0})
            self.token_dict.update({'client': 'user'})
            self.token_dict.update({'token': None})

        return self.token_dict

def main():
    argument_spec = {}
    argument_spec.update(dict(
            username=dict(required=False, type='str'),
            client_id=dict(required=False, type='str' ),
            client_secret=dict(required=False, type='str'),
            config_file=dict(required=False, type='str'),
            redirect_uri=dict(default='https://example.com/callback/',required=False, type='str'),
            scope=dict(default='',required=False, type='str')
            ))

    module = AnsibleModule(argument_spec=argument_spec)

    sp_auth = SpotifyAuthentication(module)

    if module.params.get("username"):
        results = sp_auth.user_client()
    else:
        results = sp_auth.public_client()

    module.exit_json(changed=True, results=results)

if __name__ == '__main__':
    main()
