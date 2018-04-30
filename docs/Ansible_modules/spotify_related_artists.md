# Spotify related artists

#### Modules
spotify_related_artists - Ansible module to get 20 related artists for a given artists

* Synopsis
* Options
* Examples
* Return value

#### Synopsis

Ansible module to get 20 related artists for a given artists. Artists can be provided via **name or JSON File**.
A JSON file can be generated using the Ansible module `spotify_search` or visit this site for more informations [(link)](https://beta.developer.spotify.com/documentation/web-api/reference/artists/get-artist/).

You can only define one of the options at the same time: `artists_name` or `artists_file`.
The options `dest_file` and `output_format` can be combined with all other options.

#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------|----------- |--------- | -------- |
| auth_token  | String       | Yes     | null       | null     | Spotify authentication token generated from the module `spotify_auth` and `spotify_auth_create_user_token` |
| artists_file  | String       | No     | null       | null     | JSON File containing a dict of track names.|
| artists_name  | String       | No     | null       | null     | Artists name to get the related artists for. |
| dest_file     | String       | No     | null       | null     |  Destination file to save the output to. |
| output_format  | String      | No     | long       | short, long |  Control Ansible output format. |

#### Requirements  
* python >= 2.7.10
* spotipy >= 2.4.4

#### Examples
```
- name: Get related artists name for young the giant with output_format short
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_name: young the giant
    output_format: short

- name: Get related artists name for young the giant with output_format long and save output
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_name: young the giant
    output_format: long
    dest_file: "{{ playbook_dir }}/files/related_artists.json"

- name: Get related artists from file
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_file: "{{ get_related_artists_from_file }}"

- name: Get related artists from file and save output
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_file: "{{ get_related_artists_from_file }}"
    dest_file: "{{ playbook_dir }}/files/related_artists.json"

#
# Example of how to use spotify_related_artists for a nested usage
#
- name: Get related artists for Young the giant
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_name: "Young the Giant"
    dest_file: "{{ playbook_dir }}/files/related_artists.json"

- name: Get related artists for related artists for Young the giant
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_file: "{{ playbook_dir }}/files/related_artists.json"
    dest_file: "{{ playbook_dir }}/files/related_artists.json"
```
#### RETURN VALUES:
```  
output:
  description: "Returns a dict with informations about the related artists with defined output_format short.
  returned: on success
  sample:
    changed: True
    result:
      artists:
      - uri: spotify:artist:54QMjE4toDfiCryzYWCpXX
        artist: Metronomy
      - uri: spotify:artist:6FQqZYVfTNQ1pCqfkwVFEa
        artist: Foals
  type: dict

output:
  description: "Returns a dict with informations about the related artists  with defined output_format long.
  returned: on success
  sample:
    changed: True
    result:
        artists:
            - external_urls:
                spotify: https://open.spotify.com/artist/3kVUvbeRdcrqQ3oHk5hPdx
              followers:
                href:
                total: 602082
              genres:
              - indie folk
              - indie pop
              - indie rock
              - indietronica
              - la indie
              - modern rock
              - shimmer pop
              - stomp and holler
              - synthpop
              href: https://api.spotify.com/v1/artists/3kVUvbeRdcrqQ3oHk5hPdx
              id: 3kVUvbeRdcrqQ3oHk5hPdx
              images:
              - height: 640
                url: https://i.scdn.co/image/0763ebd8606dc0a33984b7901ebdd9966d79ff24
                width: 640
              - height: 320
                url: https://i.scdn.co/image/9d6b9d1f5800063806d429bec4ad13794d548659
                width: 320
              - height: 160
                url: https://i.scdn.co/image/6463aca37297e74b497fe04cdaa00c9b87a11492
                width: 160
              name: Grouplove
              popularity: 69
              type: artist
              uri: spotify:artist:3kVUvbeRdcrqQ3oHk5hPdx
  type: dict
  ```
