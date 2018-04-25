# Spotify create authentication token

#### Modules
spotify_auth - Ansible module to creating authentication token

* Synopsis
* Options
* Examples
* Return value

#### Synopsis
Ansible module to generate a public authentication token, get a cached user authentication token from the cache file `/tmp/.cache-USER` or generate a Spotify API Code to generate a new user authentication token with the Ansible module `spotify_auth_create_user_token`.

When generating a new Spotify API Code, Ansible opens your default browser calling the `redirect_uri` e.g.

`https://example.com/callback/?code=AQBxUXgKcv3n6y3EAto3GZqFxWZkMk5m_wbt0AuTDDeA9gkyeeeydVYb6vmz-dabjsoCXE5uSh3o_NFaZFsXejs5Wr3nP4qIqQwP0wuzUDQEdqbbt8cftSLZznYHj3lhGi-UCbGgToLI00xxxslp1c6xAShITOIpjw-KdwAqCmEBMxBW8TIqavSFyur52cHDz9Ew3dD23RY-RYZOOI8VzMNs0jMtOvj6gboAF44Lesvf-1uEqr7uh239C5kjD2jE9f3l72nFXSdcT29_-kVLwQaX8jVtKW1VwYAuNe8YjzwRdNytnIP2gOqFWCM4AXuBc-9LupeHn2vkxenQ2JRPFJOiTZtFemmUWTHUE5o7juekzpAlZiZCG-IcXBV34X06NWA6GnyZYNVBXH9KIDMZck9HvL4ax5eyuha1hslLcZvgzl99YDN6orOfKXT3ewVvxiTDDIK5Mj0`

The `spotify_auth_create_user_token` only accepts the API Code which is in this case

`AQBxUXgKcv3n6y3EAto3GZqFxWZkMk5m_wbt0AuTDDeA9gkyeeeydVYb6vmz-dabjsoCXE5uSh3o_NFaZFsXejs5Wr3nP4qIqQwP0wuzUDQEdqbbt8cftSLZznYHj3lhGi-UCbGgToLI00xxxslp1c6xAShITOIpjw-KdwAqCmEBMxBW8TIqavSFyur52cHDz9Ew3dD23RY-RYZOOI8VzMNs0jMtOvj6gboAF44Lesvf-1uEqr7uh239C5kjD2jE9f3l72nFXSdcT29_-kVLwQaX8jVtKW1VwYAuNe8YjzwRdNytnIP2gOqFWCM4AXuBc-9LupeHn2vkxenQ2JRPFJOiTZtFemmUWTHUE5o7juekzpAlZiZCG-IcXBV34X06NWA6GnyZYNVBXH9KIDMZck9HvL4ax5eyuha1hslLcZvgzl99YDN6orOfKXT3ewVvxiTDDIK5Mj0`.

See section **Examples** for an full example with how to pass the API Code to the module `spotify_auth_create_user_token`.



#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------|----------- |--------- | -------- |
| username      | String      | True     |  null         | null     | Spotify Username |
| client_id     | String      | False     | null       | null     | Spotify API Client ID |
| client_secret | String      | False     | null       | null     | Spotify API Client Secret |
| redirect_uri  | String      | False     | null       | null     | Spotify redirect URL |
| scope         | String      | False     | ""         | null     | Spotify API user scope |
| config_file | String        | False     | null       | null     | Configuration file containing client_id, client_secret, redirect_uri and scope |


#### Requirements  
* python >= 2.7.10
* spotipy >= 2.4.4

#### Examples
```
# Get public Authentication token
- name: Provide client ID and client secret for Public authentication token
  spotify_auth:
    client_id: 0123456789ABCDEFGHI
    client_secret: JKLMNOPQRSTUVWXZY

# get authentication token with configuration file
- name: Provide all configuration parameters via config file
  spotify_auth:
    username: spotify_user
    config_file: "{{ inventory_dir}}/user.yaml"


# Get generated user authentication token from cache
- name: Get generated user authentication token
  spotify_auth_create_user_token:
    username: spotify_user
    api_user_code: 987654321ZYXWVUTSR
    client_id: 0123456789ABCDEFGHI
    client_secret: JKLMNOPQRSTUVWXZY
    redirect_uri: https://example.com/callback/
    scope: user-top-read,playlist-read-private

# Get generated user authentication token with configuration file from cache
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
  description: "returns a dict for a generated public authentication token"
  returned: on success
  sample:
    changed: True
    result:
      client: "public"
      token: "0123456789ABCDEFGHI"
  type: dict

output:
  description: "returns a dict for a cached user authentication token"
  returned: on success
  sample:
    changed: True
    result:
      cached: true
      client: "user"
      token: "0123456789ABCDEFGHI"
  type: dict

  output:
    description: "returns a dict for a non cached user authentication token"
    returned: on success
    sample:
      changed: True
      result:
        cached: false
        client: "user"
        token: "null
    type: dict
```
