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

`http://mbloch.s3-website-ap-southeast-2.amazonaws.com/?code=AQDFYVg0pC7YF4rZ1bMApVXNrhbjQn9QPJWRJxs6HmE8eksQgZpyXdKiQIXHgN_5j7lfE6BEZ_asdfasfdMo4Ps0fwep98GZvcvbczvasdfQOPNLx71mA0bmlA3IveCmKLs61qIO_OjAYa8P8a4DSKdtN123123123s6cGCRZ_JElumBELi-aa6e0QQ5hsEX5s1Md9OTf2tO_n5Wy7MUXP-jJBwMUNLUSeP_KG09LCaokpUHXtN5D__-q-S9NJbmYFiCrd8M6J9Cv6EzxcvzxcvzxcvLc8CeCCeQSAuJnl7ZaYY9DYNlZyvYOaoCXM2Ooo7NEtXxvLG-suC3hiMq-siK0hntGbG_1yRWa1jtGAdHOp-Nst9xEMKxvnOKtwOnq_g1Pd7asdfasdft_nioWT9KRL8ooIw2hwSrzhAG4L0y79vu9_KI1mGvQPaYpwQ`

The `spotify_auth_create_user_token` only accepts the API Code which is in this case

`AQDFYVg0pC7YF4rZ1bMApVXNrhbjQn9QPJWRJxs6HmE8eksQgZpyXdKiQIXHgN_5j7lfE6BEZ_asdfasfdMo4Ps0fwep98GZvcvbczvasdfQOPNLx71mA0bmlA3IveCmKLs61qIO_OjAYa8P8a4DSKdtN123123123s6cGCRZ_JElumBELi-aa6e0QQ5hsEX5s1Md9OTf2tO_n5Wy7MUXP-jJBwMUNLUSeP_KG09LCaokpUHXtN5D__-q-S9NJbmYFiCrd8M6J9Cv6EzxcvzxcvzxcvLc8CeCCeQSAuJnl7ZaYY9DYNlZyvYOaoCXM2Ooo7NEtXxvLG-suC3hiMq-siK0hntGbG_1yRWa1jtGAdHOp-Nst9xEMKxvnOKtwOnq_g1Pd7asdfasdft_nioWT9KRL8ooIw2hwSrzhAG4L0y79vu9_KI1mGvQPaYpwQ`.

Open this link to see an example [link example](http://mbloch.s3-website-ap-southeast-2.amazonaws.com/?code=AQDFYVg0pC7YF4rZ1bMApVXNrhbjQn9QPJWRJxs6HmE8eksQgZpyXdKiQIXHgN_5j7lfE6BEZ_asdfasfdMo4Ps0fwep98GZvcvbczvasdfQOPNLx71mA0bmlA3IveCmKLs61qIO_OjAYa8P8a4DSKdtN123123123s6cGCRZ_JElumBELi-aa6e0QQ5hsEX5s1Md9OTf2tO_n5Wy7MUXP-jJBwMUNLUSeP_KG09LCaokpUHXtN5D__-q-S9NJbmYFiCrd8M6J9Cv6EzxcvzxcvzxcvLc8CeCCeQSAuJnl7ZaYY9DYNlZyvYOaoCXM2Ooo7NEtXxvLG-suC3hiMq-siK0hntGbG_1yRWa1jtGAdHOp-Nst9xEMKxvnOKtwOnq_g1Pd7asdfasdft_nioWT9KRL8ooIw2hwSrzhAG4L0y79vu9_KI1mGvQPaYpwQ)

See section **Examples** for a full example with how to pass the API Code to the module `spotify_auth_create_user_token`.



#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------|----------- |--------- | -------- |
| username      | String      | Yes     |  null         | null     | Spotify Username |
| client_id     | String      | No     | null       | null     | Spotify API Client ID |
| client_secret | String      | No     | null       | null     | Spotify API Client Secret |
| redirect_uri  | String      | No     | http://mbloch.s3-website-ap-southeast-2.amazonaws.com       | null     | Spotify redirect URL |
| scope         | String      | No     | ""         | null     | Spotify API user scope |
| config_file | String        | No     | null       | null     | Configuration file containing client_id, client_secret, redirect_uri and scope |


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
    redirect_uri: http://mbloch.s3-website-ap-southeast-2.amazonaws.com
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
