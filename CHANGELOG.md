# 0.0.7 - 04-26-2018
### ADDED
* Extend functionallity of the Ansible module spotify_player. It now supports to play tracks, albums, playlist or tracks from an artist. See Documentation and examples for how to use.

### MODIFIED
* Improved file/dict handling in several Ansible modules
* Update spotify_player module documentation
* Update spotify_player roles

# 0.0.6 - 04-25-2018
### ADDED
* New redirect URL
* Example HTML file to use for your redirect_url

### MODIFIED
* Improved Documentation for each Ansible Module.
* Relocated example playbooks.
* Made the Ansible modules Ansible PEP8 friendly.

# 0.0.5 - 04-21-2018
### ADDED
* New Ansible module to update a user playlist (Add & remove tracks)
* Feature to transfer playback to a different device with module spotify_player
* Added Ansible module documentation
* Integration test of all roles and states


### MODIFIED
* Renamed Ansible module sp_auth to sptify_auth
* Renamed Ansible module sp_auth_create_user_token to spotify_auth_create_user_token
* Improved Ansible module documentation
* Renamed Ansible module option for output format full to long
* Moved tasks from Ansible module user_tracks module to module spotify_user_info
* Moved example playbooks to folder examples

### Removed
* Ansible user_tracks module

# 0.0.4 - 04-18-2018
### MODIFIED
* Improved module documentation
* Improved module JSON short format output
* Changed default Ansible module output behaviour to full output

### Removed
* Dependency to custom python library

# 0.0.3 - 04-17-2018
### MODIFIED
* Updated module documentation

### ADDED
* Spotify Player role for tasks play, pause, next, previous, set volume, toggle shuffle, toggle repeat
* Get User info
* Get Current played track, recently played tracks, get top played artists, get top played tracks

# 0.0.2 - 04-16-2018
### ADDED
* Search for Artists
* Search for Tracks
* Search for Albums
* Search for Playlists
* Search for Artists + Tracks
* Search for Artists + Albums

# 0.0.1 - 04-15-2018
### ADDED
- User and Public API authentication
- Get top tracks from one or more artists
- Get related artists from one ore more artists
- Get user playlists
- Create user playlists
