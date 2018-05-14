# Synopsis:
An Ansible client to interact with the Spotify API

# Prerequisites:
* Ansible 2.5
* Python 2.7.10
* Spotipy 2.4.4 from [Github/Spotipy](https://github.com/plamere/spotipy)

`pip install git+https://github.com/plamere/spotipy.git --upgrade`

* Spotify Account [Spotify](https://spotify.com)
* Spotify API Client ID [Developer Spotify](https://developer.spotify.com/dashboard/login)

# Usage:

* Modify variables in 'ansible/inventory/group_vars/all.yaml' and or 'ansible/inventory/group_vars/user.yaml'  to own needs.
  - client_id = Spotify API Client ID
  - client_secret = Spotify API Client secret
  - redirect_uri: e.g. http://mbloch.s3-website-ap-southeast-2.amazonaws.com
  - scope: Depends on role using [more information](https://developer.spotify.com/web-api/using-scopes/)
  - Update Ansible Playbooks to your own need

* Modify example playbooks to own need

### Using the example playbooks

Have a look to the example folder. Here are some example using the roles:

Control your Spotify with the Spotify Player( Play, Pause, Next, Previous, Toggle shuffle, toggle repeat or set the volume):
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook -v examples/spotify_player.yaml
```

Get Releated artists name:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook -v examples/spotify_get_related_artists.yaml
```

Get Artists top tracks:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook -v examples/spotify_get_artists_top_tracks.yaml
```

Get Audio features about a track:
```
ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook -v examples/spotify_track_data/track_feature_from_track_id.yaml
```

Get Audio analyse data about a track:
```
ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook -v examples/spotify_track_data/track_analyse_from_track_id.yaml
```
Create a user playlist:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook -v examples/spotify_user_playlists/spotify_user_playlists_crete.yaml
```

Search for an Album:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook -v examples/spotify_search/spotify_search_albums.yaml
```

Search for Artist and Album in combination:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook -v examples/spotify_search/spotify_search_artists_and_albums.yaml
```

Get users top-tracks:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook -v examples/spotify_user_info/spotify_user_info_top_tracks.yaml
```

Example of getting top tracks of related artists, create a new playlist and add the top tracks to it.
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook -v examples/spotify_save_top_tracks_of_related_artists_to_create_playlist.yaml
```

# Documentation:

### Authentication

Detail information about the authentication process can be found here [(link)](https://pillpall.github.io/ansible/2018/04/28/Use-Ansible-to-automate-Spotify-part-I.html).

User client authentication:

 For User Authentication you need to define all parameters in `ansible/inventory/group_vars/user.yaml` and run a role.


Public client authentication:

 For User Authentication you need to define all parameters in `ansible/inventory/group_vars/public.yaml` and run a role.

Callback URL:
 An example HTML File for your own redirect_uri can be found in **examples/callback**. Use this file as your redirect_uri to make it easier to copy/paste the API User code. See this example: [link example](http://mbloch.s3-website-ap-southeast-2.amazonaws.com/?code=AQDFYVg0pC7YF4rZ1bMApVXNrhbjQn9QPJWRJxs6HmE8eksQgZpyXdKiQIXHgN_5j7lfE6BEZ_asdfasfdMo4Ps0fwep98GZvcvbczvasdfQOPNLx71mA0bmlA3IveCmKLs61qIO_OjAYa8P8a4DSKdtN123123123s6cGCRZ_JElumBELi-aa6e0QQ5hsEX5s1Md9OTf2tO_n5Wy7MUXP-jJBwMUNLUSeP_KG09LCaokpUHXtN5D__-q-S9NJbmYFiCrd8M6J9Cv6EzxcvzxcvzxcvLc8CeCCeQSAuJnl7ZaYY9DYNlZyvYOaoCXM2Ooo7NEtXxvLG-suC3hiMq-siK0hntGbG_1yRWa1jtGAdHOp-Nst9xEMKxvnOKtwOnq_g1Pd7asdfasdft_nioWT9KRL8ooIw2hwSrzhAG4L0y79vu9_KI1mGvQPaYpwQ).



### Modules

| Module name                    | Description                                | Documentation |
| ------------------------------ | ------------------------------------------ | ------------- |
| spotify_auth                   | Module for the authentication process      |[Link](https://github.com/PillPall/ansible-spotify-client/blob/master/docs/Ansible_modules/spotify_auth.md)|
| spotify_auth_create_user_token | Module for the user authentication process |[Link](https://github.com/PillPall/ansible-spotify-client/blob/master/docs/Ansible_modules/spotify_auth_create_user_token.md)|
| spotify_album     | Get information about one or multiple albums. |[Link](https://github.com/PillPall/ansible-spotify-client/blob/master/docs/Ansible_modules/spotify_album.md)|
| spotify_artists_top_tracks     | Get the top tracks of an artist            |[Link](https://github.com/PillPall/ansible-spotify-client/blob/master/docs/Ansible_modules/spotify_artists_top_tracks.md)|
| spotify_player                 | Spotify Player to play a song and more.    |[Link](https://github.com/PillPall/ansible-spotify-client/blob/master/docs/Ansible_modules/spotify_player.md)|
| spotify_related_artists        | Get related artists                        | [Link](https://github.com/PillPall/ansible-spotify-client/blob/master/docs/Ansible_modules/spotify_related_artists.md)|
| spotify_search                 | Search in Spotify                          | [Link](https://github.com/PillPall/ansible-spotify-client/blob/master/docs/Ansible_modules/spotify_search.md)|
| spotify_track_data     | Get Audio features from a track or analyse tracks  | [Link](https://github.com/PillPall/ansible-spotify-client/blob/master/docs/Ansible_modules/spotify_artists_top_tracks.md)|
| spotify_user_info              | Get user information                       | [Link](https://github.com/PillPall/ansible-spotify-client/blob/master/docs/Ansible_modules/spotify_user_info.md)|
| spotify_user_playlists         | Search and create a user playlist          | [Link](https://github.com/PillPall/ansible-spotify-client/blob/master/docs/Ansible_modules/spotify_user_playlists.md)|
| spotify_update_playlists       | Add or remove songs from a playlist        | [Link](https://github.com/PillPall/ansible-spotify-client/blob/master/docs/Ansible_modules/spotify_update_playlists.md)|

### Examples
Examples can be found in the directory **examples**.

### Roles
All Roles for using the Ansible Modules can be found in the directory **roles**.

# TO-DOs:
[TO-DOs](./TODO.md)

# Changelog:
[Changelog](./CHANGELOG.md)

# Contributing:
For any questions use github or email: github@mbloch.de
