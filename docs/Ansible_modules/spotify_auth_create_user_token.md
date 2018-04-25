# Spotify authentication create user token

#### Modules
spotify_auth_create_user_token - Ansible module to create user authentication token for Spotify API

* Synopsis
* Options
* Examples
* Return value

#### Synopsis
Ansible module to create a User authentication token generated from the Ansible module `spotify_auth`.

Option `api_user_code` & `username` has to be defined **everytime**. Options `client_id, client_secret, redirect_uri, and scope` has to be provided via option parameter in the task or the configuration file option `config_file`.

To Acess User data you need to specify a specific scope. For more information about available scopes visit this site  [link](https://beta.developer.spotify.com/documentation/general/guides/scopes/).

#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------|----------- |--------- | -------- |
| api_user_code | String      | Yes     | null       | null     | Spotify API User code |
| username      | String      | Yes     |  null         | null     | Spotify Username |
| client_id     | String      | No     | null       | null     | Spotify API Client ID |
| client_secret | String      | No     | null       | null     | Spotify API Client Secret |
| redirect_uri  | String      | No     | null       | null     | Spotify redirect URL |
| scope         | String      | No     | ""         | null     | Spotify API user scope |
| config_file | String        | No     | null       | null     | Configuration file containing client_id, client_secret, redirect_uri and scope |

#### Requirements  
* python >= 2.7.10
* spotipy >= 2.4.4

#### Examples
```
# Generate a new user authentication token
- name: Get generated user authentication token
  spotify_auth_create_user_token:
    username: spotify_user
    api_user_code: 987654321ZYXWVUTSR
    client_id: 0123456789ABCDEFGHI
    client_secret: JKLMNOPQRSTUVWXZY
    redirect_uri: https://example.com/callback/
    scope: user-top-read,playlist-read-private

# Generate a new user authentication token with configuration file
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
```
#### RETURN VALUES:
```  
output:
  description: "returns a dict type with the authentication token for the Spotify API."
  returned: on success
  sample:
    changed: True
    result:
      client: "user"
      token: "0123456789ABCDEFGHI"
  type: dict
  ```
