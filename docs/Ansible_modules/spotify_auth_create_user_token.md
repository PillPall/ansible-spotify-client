> SPOTIFY_AUTH_CREATE_USER_TOKEN    (./ansible/library/spotify_auth_create_user_token.py)

        Ansible module for authentication with the Spotify API.

OPTIONS (= is mandatory):

= api_user_code
        Spotify API User Code

        type: String

- client_id
        Spotify API Client ID
        [Default: (null)]
        type: String

- client_secret
        Spotify API Client Secret Key
        [Default: (null)]
        type: String

- config_file
        Configuration file containing Spotify API Authentication parameters
        [Default: (null)]
        type: String

- redirect_uri
        Redirect URL, required for user authentication
        [Default: (null)]
        type: String

- scope
        Scope, required for User authentication. For avaiable scopes visit https://beta.developer.spotify.com/documentation/general/guides/scopes/.
        [Default: (null)]
        type: String

- username
        Spotify Username required for user authentication
        [Default: (null)]
        type: String


REQUIREMENTS:  python >= 2.7.10, spotipy >= 2.4.4

AUTHOR: Michael Bloch (github@mbloch.de)
        METADATA:
          status:
          - preview
          supported_by: community


EXAMPLES:
# Get generated user authentication token
- name: Get generated user authentication token
  spotify_auth_create_user_token:
    username: spotify_user
    api_user_code: 987654321ZYXWVUTSR
    client_id: 0123456789ABCDEFGHI
    client_secret: JKLMNOPQRSTUVWXZY
    redirect_uri: https://example.com/callback/
    scope: user-top-read,playlist-read-private

# Get generated user authentication token with configuration file
- name: Provide all configuration parameters via config file
  spotify_auth_create_user_token:
    username: spotify_user
    api_user_code: 987654321ZYXWVUTSR
    config_file: "{{ inventory_dir}}/user.yaml"

An example of how to get a user authenticaton token from Cache or a generated one:

# Get user authentication token
- name: Provide all options for user authentication token
  spotify_auth:
    username: spotify_user
    client_id: 0123456789ABCDEFGHI
    client_secret: JKLMNOPQRSTUVWXZY
    redirect_uri: https://example.com/callback/
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

RETURN VALUES:


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
