#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: sp_auth
short_description: Ansible module for authentication with the Spotify API.
description:
    - "Ansible module for authentication with the Spotify API.
      This module Connects to the Spotify API and response with an
      Authentiaction token. To get a new generated User token you need
      to provide the generated API Code to the Ansible Module sp_auth_create_user_token.
      You will get this API Code from your Browser which this Ansible module will openselfself.
      Visit https://github.com/PillPall/ansible-spotify-client for an example."

version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)
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

requirements:
- python >= 2.7.10
- spotipy >= 2.4.4
'''

EXAMPLES = '''
# Get public Authentication token
- name: Provide client ID and client secret for Public authentication token
  sp_auth:
    client_id=0123456789ABCDEFGHI
    client_secret=JKLMNOPQRSTUVWXZY

# Get user authentication token
- name: Provide all options for user authentication token
  sp_auth:
    username: spotify_user
    client_id=0123456789ABCDEFGHI
    client_secret=JKLMNOPQRSTUVWXZY
    redirect_uri=https://example.com/callback/
    scope=user-top-read,playlist-read-private

# get authentication token with configuration file
- name: Provide all configuration parameters via config file
  sp_auth:
    username: spotify_user
    config_file="{{ inventory_dir}}/user.yaml"
'''
RETURN = '''
---
output:
  description: "returns a dict type with the authentication token for the Spotify API.
  When requesting a user authentication token it additional displays if it used a cached token or not."
  returned: always
  sample:
    changed: True
    result:
      cached: True
      client: "user"
      token: "0123456789ABCDEFGHI"
  type: dict
'''



import sys
import os
import yaml
import json
from ansible.module_utils.basic import *

try:
    import spotipy.oauth2 as oauth2
except ImportError as e:
    module.fail_json(msg="Error: Can't import required libraries - " + str(e))

class SpotifyAuthentication:
    def __init__(self, module):
        self.module = module
        self.token_dict = {}

    def create_config(self):
        if self.module.params.get("config_file"):
            created_config = self.read_config()
        elif self.module.params.get("client_id") and self.module.params.get("client_secret"):
            client_id = self.module.params.get("client_id")
            client_secret = self.module.params.get("client_secret")
            created_config = self.build_config(client_id, client_secret)
        elif os.getenv('SPOTIPY_CLIENT_ID') and os.getenv('SPOTIPY_CLIENT_SECRET'):
            client_id = os.getenv('SPOTIPY_CLIENT_ID')
            client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
            created_config = self.build_config(client_id, client_secret)
        else:
            self.module.fail_json(msg="Error: Can't find credentials")

        return created_config

    def build_config(self, client_id, client_secret):
        conf = {}
        conf.update({'client_id': client_id})
        conf.update({'client_secret': client_secret})
        if self.module.params.get("username"):
                conf.update({'username': self.module.params.get("username")})
                conf.update({'redirect_uri': self.module.params.get("redirect_uri")})
                conf.update({'scope': self.module.params.get("scope")})

    def read_config(self):
        config_file = self.module.params.get("config_file")
        with open(config_file, 'r') as ymlfile:
            conf = yaml.load(ymlfile)

        return conf

    def public_client(self):

        conf = self.create_config()
        credentials = oauth2.SpotifyClientCredentials(**conf)
        try:
            token = credentials.get_access_token()
            self.token_dict.update({'client': 'public'})
            self.token_dict.update({'token': token})
            return self.token_dict

        except Exception as e:
            self.module.fail_json(msg="Error: Can't finish authentication - " + str(e))

    def user_client(self):
        conf = self.create_config()
        username = self.module.params.get("username")
        cache_path = "/tmp/.cache-" + username
        sp_oauth = oauth2.SpotifyOAuth(cache_path=cache_path, **conf)
        token_info = sp_oauth.get_cached_token()

        if token_info:
            token = token_info['access_token']
            self.token_dict.update({'cached': True})
            self.token_dict.update({'client': 'user'})
            self.token_dict.update({'token': token})
        else:
            auth_url = sp_oauth.get_authorize_url()
            try:
                import webbrowser
                webbrowser.open(auth_url)

            except Exception as e:
                self.module.fail_json(msg="Error: Can't open browser for authentication - " + str(e))

            self.token_dict.update({'cached': False})
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
