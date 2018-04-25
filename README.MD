# Synopsis:
An Ansible client to interact with the Spotify API

# Prerequisites:
* Ansible 2.5
* Python 2.7.10
* Spotipy 2.4.4 from [Spotipy](https://github.com/plamere/spotipy)
* Spotify Account [Spotify](https://spotify.com)
* Spotify API Client ID [Developer Spotify](https://developer.spotify.com/dashboard/login)

# Usage:

* Modify variables in 'ansible/inventory/group_vars/all.yaml' and or 'ansible/inventory/group_vars/user.yaml'  to own needs.
  - client_id = Spotify API Client ID
  - client_secret = Spotify API Client secret
  - redirect_uri: For testing purpose use https://example.com/callback/
  - scope: Depends on role using[More information](https://developer.spotify.com/web-api/using-scopes/)
  - Update Ansible Playbooks to your own need

* Modify example playbooks to own need


### Documentation
Documentation about all Ansible modules can be found under the directory **docs**.

Examples can be found in the directory **examples**.

All Roles to use the Ansible Modules can be found in the directory **roles**.

### Using the example playbooks

Have a look to the example folder. Here are some example commands:

Control your Spotify with the Spotify Player( Play, Pause, Next, Previous, Toggle shuffle, toggle repeat or set the volume):
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook examples/spotify_player.yaml
```

Get Releated artists name:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook examples/spotify_get_related_artists.yaml
```

Get Artists top tracks:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook examples/spotify_get_artists_top_tracks.yaml
```

Create a user playlist:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook examples/spotify_user_playlists/spotify_user_playlists_crete.yaml
```


Search for an Album:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook examples/spotify_search/spotify_search_albums.yaml
```

Search for Artist and Album in combination:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook examples/spotify_search/spotify_search_artists_and_albums.yaml
```

tracks:
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook examples/spotify_user_info/spotify_user_info_top_tracks.yaml
```

Example of getting top tracks of related artists, create a new playlist and add the top tracks to it.
```
# ANSIBLE_CONFIG=ansible/config/ansible.cfg ansible-playbook examples/spotify_save_top_tracks_of_related_artists_to_create_playlist.yaml
```

# Notes

User client authentication:


 For User Authentication you need to define all parameters in `ansible/inventory/group_vars/user.yaml` and run a role.
 If no user authentication happens before Ansible is going to `pause and wait for input` and opens your default Browser directing to the Spotify authentication page. Next you need to login to spotify and allow the application access. After allowing, you will be redirected to the URL specified in `redirect_uri` similar to
 `https://example.com/callback/?code=AQCe4xO4qobzsv2zfF5MfvNrk5Etq3QA-hljy40wMoy3PGQwCYR3wVdrYS9a2jC8gqKbjRXvw5-8ooV9RI8WrNp0m6bseWNB0TCjMyAhF-4mXg13sjx42Y468KB5BNAsSptj7ekG5gRYNHQ9CAE74tt89izbtMlYZ0D_tSPw7xbTHhKtM7gYusA9F4yep0RfhiYSJs6O1nD7rfrNfN2KOqRKw_kP86DTNaZVFQ`

 Now you need to copy the Part of the URL after `code=` e.g. `AQCe4xO4qobzsv2zfF5MfvNrk5Etq3QA-hljy40wMoy3PGQwCYR3wVdrYS9a2jC8gqKbjRXvw5-8ooV9RI8WrNp0m6bseWNB0TCjMyAhF-4mXg13sjx42Y468KB5BNAsSptj7ekG5gRYNHQ9CAE74tt89izbtMlYZ0D_tSPw7xbTHhKtM7gYusA9F4yep0RfhiYSJs6O1nD7rfrNfN2KOqRKw_kP86DTNaZVFQ` and paste it to the command line, which waits for your input. Ansible will then create a cache file with your credentials `/tmp/.cache-USERNAME` e.g. `/tmp/.cache-bloch-m`. Once your credentials are cached there is no need to redo the authentication unless your credentials are expired.


Public client authentication:


You only need to provide a Client ID and Secret Key. Since we connect here to the Public interface there is no need for extra authentication.


# TO-DOs:
[TO-DOs](./TODO.md)

# Changelog:
[Changelog](./CHANGELOG.md)

# Contributing:
For any questions use github or email: github@mbloch.de
