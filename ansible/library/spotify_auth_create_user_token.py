#!/usr/bin/python
# -*- coding: utf8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: spotify_auth_create_user_token
short_description: Ansible module to create user authenticatio token
description:
    - "Ansible module for authentication with the Spotify API."

version_added: "2.5"

author:
    - Michael Bloch (github@mbloch.de)

options:
    api_user_code:
       description:
         - Spotify API User Code
       required: True
       type: String

    client_id:
       description:
         - Spotify API Client ID
       type: String

    client_secret:
       description:
         - Spotify API Client Secret Key
       type: String

    config_file:
       description:
         - Configuration file containing Spotify API Authentication parameters
       type: String

    redirect_uri:
       description:
         - Redirect URL, required for user authentication
       type: String

    scope:
       description:
         - Scope, required for User authentication.
       type: String

    username:
       description:
         - Spotify Username required for user authentication
       type: String

requirements:
- python >= 2.7.10
- spotipy >= 2.4.4
'''

EXAMPLES = '''
# Get generated user authentication token
- name: Get generated user authentication token
  spotify_auth_create_user_token:
    username: spotify_user
    api_user_code: 987654321ZYXWVUTSR
    client_id: 0123456789ABCDEFGHI
    client_secret: JKLMNOPQRSTUVWXZY
    redirect_uri: http://mbloch.s3-website-ap-southeast-2.amazonaws.com
    scope: user-top-read,playlist-read-private

# Get generated user authentication token with configuration file
- name: Provide all configuration parameters via config file
  spotify_auth_create_user_token:
    username: spotify_user
    api_user_code: 987654321ZYXWVUTSR
    config_file: "{{ inventory_dir}}/user.yaml"

#
# A full example of how to get a user authenticaton token from Cache or a generate a new one:
#
# Get user authentication token
- name: Provide all options for user authentication token
  spotify_auth:
    username: spotify_user
    client_id: 0123456789ABCDEFGHI
    client_secret: JKLMNOPQRSTUVWXZY
    redirect_uri: http://mbloch.s3-website-ap-southeast-2.amazonaws.com
    scope: user-top-read,playlist-read-private
  register: sp_user_auth

- name: Wait for User to type in the User API Code
  pause:
    prompt: "Please type in the SP API User Code"
    echo: yes
  register: _sp_api_user_code
  when: not sp_user_auth.results.cached

- name: Set Spotify API user code
  set_fact:
    sp_api_user_code: "{{_sp_api_user_code.user_input}}"
  when: _sp_api_user_code.skipped is undefined

- name: Create user token from Spotify API user code
  spotify_auth_create_user_token:
    api_user_code: "{{ sp_api_user_code }}"
    username: "{{ username }}"
    config_file: "{{ config_file }}"
  register: _sp_user_auth
  when: sp_api_user_code is defined

# Set cached user token as auth_token
- name: Set cached user token as auth_token
  set_fact:
    auth_token: "{{ sp_user_auth.results.token }}"
  when: _sp_user_auth.skipped is defined and sp_user_auth.results is defined

# Set generated user token as auth_token
- name: Set generated user token as auth_token
  set_fact:
    auth_token: "{{ _sp_user_auth.results.token }}"
  when: _sp_user_auth.skipped is undefined
'''
RETURN = '''
---
output:
  description: "returns a dict type with the authentication token for the Spotify API."
  returned: on success
  sample:
    changed: True
    result:
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


class UserTokenCreation:
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

    def create_user_token(self):
        conf = self.create_config()
        api_user_code = self.module.params.get("api_user_code")
        username = self.module.params.get("username")
        cache_path = "/tmp/.cache-" + username
        try:
            sp_oauth = oauth2.SpotifyOAuth(cache_path=cache_path, **conf)
            token_info = sp_oauth.get_access_token(api_user_code)
            token = token_info['access_token']
            self.token_dict.update({'client': 'user'})
            self.token_dict.update({'token': token})
        except Exception as e:
            self.module.fail_json(msg="Error: Can't get user token - " + str(e))

        return self.token_dict


def main():
    argument_spec = {}
    argument_spec.update(dict(
        api_user_code=dict(required=True, type='str'),
        client_id=dict(required=False, type='str'),
        client_secret=dict(required=False, type='str'),
        config_file=dict(required=False, type='str'),
        redirect_uri=dict(defualt='http://mbloch.s3-website-ap-southeast-2.amazonaws.com', required=False, type='str'),
        scope=dict(defualt='', required=False, type='str'),
        username=dict(required=True, type='str')
    ))

    module = AnsibleModule(argument_spec=argument_spec)

    sp_user_token = UserTokenCreation(module)
    results = sp_user_token.create_user_token()

    module.exit_json(changed=True, results=results)

if __name__ == '__main__':
    main()
