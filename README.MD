# Synopsis:
An Ansible client to interact with the Spotify API

# Prerequisets:
* Ansible 2.5
* Python 2.7.10
* Spotipy 2.4.4 [Spotipy](https://github.com/plamere/spotipy)
* Spotify Account [Spotify](https://spotify.com)
* Spotify API Client ID [Developer Spotify](https://developer.spotify.com/dashboard/login)

# Usage:

* Modify variables in 'ansible/inventory/group_vars/all.yaml' and or 'ansible/inventory/group_vars/user.yaml'  to own needs.
  - client_id = Spotify API Client ID
  - client_secret = Spotify API Client secret
  - redirect_uri: For testing purpose use https://example.com/callback/
  - scope: Depends on role using[More information](https://developer.spotify.com/web-api/using-scopes/)

Get Releated artists name:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook spotify_get_related_artists.yaml -i ansible/inventory/hosts --module-path ansible/library/
```

Get Artists top tracks:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook spotify_get_artists_top_tracks.yaml -i ansible/inventory/hosts --module-path ansible/library/
```

Get users playlist:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook spotify_get_user_playlists.yaml -i ansible/inventory/hosts --module-path ansible/library/
```

Create a user playlist:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook spotify_create_user_playlists.yaml -i ansible/inventory/hosts --module-path ansible/library/
```

# Notes
User client authentication:

Public client authentication:

# TO-DOs:
[TO-DOs](./TODO.md)

# Changelog:
[Changelog](./CHANGELOG.md)

# Contributing:
For any questions use github or email: github@mbloch.de
