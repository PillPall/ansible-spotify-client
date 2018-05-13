# Spotify Album

#### Modules
spotify_album - Ansible module to query for album informations

* Synopsis
* Options
* Examples
* Return value

#### Synopsis

Ansible module to query for all album information or only album tracks. Albums can be provided via **URI or JSON File**.

A JSON file can be generated using the Ansible module `spotify_search`. For more informaiton visit this link [link](https://beta.developer.spotify.com/documentation/web-api/reference/object-model/#album-object-simplified).

You can only define one of the option `album_file` and `album_uri` options.

The options `dest_file`, `limit` and `output_format` can be combined with all states.

Informations about the output format can be found here [link](https://beta.developer.spotify.com/documentation/web-api/reference/albums/get-albums-tracks/).

#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------- | -------- |--------- | -------- |
| auth_token    | String      | Yes        | null     | null     | Spotify authentication token generated from the module `spotify_auth` and `spotify_auth_create_user_token` |
| state         | String      | Yes        |     null | album, album_tracks| Action to trigger. |
| album_uri     | String      | No         | null     | null     | Album URI. |
| album_file | String | No | null | null | JSON File containing a dict of album URIs. |
| limit | String | No | null | null | Limit the search output. |
| dest_file     | String       | No     | null       | null     |  Destination file to save the output to. |
| output_format  | String      | No     | long       | short, long |  Control Ansible output format. |

#### Requirements  
* python >= 2.7.10
* spotipy >= 2.4.4

#### Examples
```
- name: Get information about an album and return only the first 10 tracks.
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: short
    state: album
    album_uri: 4aawyAB9vmqN3uQ7FjRGTy
    limit: 10
  register: album_information

- name: Get all album tracks.
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: long
    state: album_tracks
    album_uri: 4aawyAB9vmqN3uQ7FjRGTy
  register: album_tracks

- name: Get all album informations from all albums given with a file.
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: short
    state: album
    album_file: "{{playbook_dir}}/search_result_artists_albums.json"
  register: album_information

- name: Get all album tracks from all albums given with a file.
  spotify_search:
    auth_token: 0123456789ABCDEFGHI
    output_format: long
    state: album_tracks
    album_file: "{{playbook_dir}}/search_result_artists_albums.json"
  register: album_tracks
```

#### RETURN VALUES:
```
---
output:
  description: "returns a dict with all information about an album long output"
  returned: on success
  sample:
    changed: True
    result:
        album_type: album
            artists:
            - external_urls:
                spotify: https://open.spotify.com/artist/3zD5liDjbqljSRorrrcEjs
              href: https://api.spotify.com/v1/artists/3zD5liDjbqljSRorrrcEjs
              id: 3zD5liDjbqljSRorrrcEjs
              name: Guillemots
              type: artist
              uri: spotify:artist:3zD5liDjbqljSRorrrcEjs
            available_markets:
            - AD
            - AR
            - AT
            - AU
            - BE
            - BG
            - BO
            - BR
            - CA
            - CH
            - CL
            - CO
            - CR
            - CY
            - CZ
            - DE
            - DK
            - DO
            - EC
            - EE
            - ES
            - FI
            - FR
            - GB
            - GR
            - GT
            - HK
            - HN
            - HU
            - ID
            - IE
            - IL
            - IS
            - IT
            - JP
            - LI
            - LT
            - LU
            - LV
            - MC
            - MT
            - MX
            - MY
            - NI
            - NL
            - 'NO'
            - NZ
            - PA
            - PE
            - PH
            - PL
            - PT
            - PY
            - RO
            - SE
            - SG
            - SK
            - SV
            - TH
            - TR
            - TW
            - US
            - UY
            - VN
            - ZA
            copyrights:
            - text: 2012 The state51 Conspiracy Ltd
              type: C
            - text: 2012 The state51 Conspiracy Ltd
              type: P
            external_ids:
              upc: '5055453648229'
            external_urls:
              spotify: https://open.spotify.com/album/1NAThLIEnLUCWXAQLWVxnR
            genres: []
            href: https://api.spotify.com/v1/albums/1NAThLIEnLUCWXAQLWVxnR
            id: 1NAThLIEnLUCWXAQLWVxnR
            images:
            - height: 640
              url: https://i.scdn.co/image/bf5c7e8afcf369da44657b2c1dd1a3cb657608b4
              width: 640
            - height: 300
              url: https://i.scdn.co/image/a19086f9263c84c1f276bb89949534064f63800f
              width: 300
            - height: 64
              url: https://i.scdn.co/image/36c8ae4e633ff8d55422ed1f0ff7f710c53c0462
              width: 64
            label: The state51 Conspiracy
            name: Hello Land!
            popularity: 19
            release_date: '2012-05-08'
            release_date_precision: day
            tracks:
              href: https://api.spotify.com/v1/albums/1NAThLIEnLUCWXAQLWVxnR/tracks?offset=0&limit=50
              items:
              [...]
              - artists:
                - external_urls:
                    spotify: https://open.spotify.com/artist/3zD5liDjbqljSRorrrcEjs
                  href: https://api.spotify.com/v1/artists/3zD5liDjbqljSRorrrcEjs
                  id: 3zD5liDjbqljSRorrrcEjs
                  name: Guillemots
                  type: artist
                  uri: spotify:artist:3zD5liDjbqljSRorrrcEjs
                available_markets:
                - AD
                - AR
                - AT
                - AU
                - BE
                - BG
                - BO
                - BR
                - CA
                - CH
                - CL
                - CO
                - CR
                - CY
                - CZ
                - DE
                - DK
                - DO
                - EC
                - EE
                - ES
                - FI
                - FR
                - GB
                - GR
                - GT
                - HK
                - HN
                - HU
                - ID
                - IE
                - IL
                - IS
                - IT
                - JP
                - LI
                - LT
                - LU
                - LV
                - MC
                - MT
                - MX
                - MY
                - NI
                - NL
                - 'NO'
                - NZ
                - PA
                - PE
                - PH
                - PL
                - PT
                - PY
                - RO
                - SE
                - SG
                - SK
                - SV
                - TH
                - TR
                - TW
                - US
                - UY
                - VN
                - ZA
                disc_number: 1
                duration_ms: 366786
                explicit: false
                external_urls:
                  spotify: https://open.spotify.com/track/59rLnKec0He0mSt9PxmNoU
                href: https://api.spotify.com/v1/tracks/59rLnKec0He0mSt9PxmNoU
                id: 59rLnKec0He0mSt9PxmNoU
                is_local: false
                name: I Lie Down
                preview_url: https://p.scdn.co/mp3-preview/b02526e8b5a9b3dd70edfaa51911668c5e7b058e?cid=a430d21d72594499a3aaee8dc9636a3f
                track_number: 8
                type: track
                uri: spotify:track:59rLnKec0He0mSt9PxmNoU
              limit: 50
              next: null
              offset: 0
              previous: null
              total: 8
            type: album
            uri: spotify:album:1NAThLIEnLUCWXAQLWVxnR
  type: dict

output:
  description: "returns a dict with all information about an album short output"
  returned: on success
  sample:
    changed: True
    result:
        album:
            - name: Global Warming
              uri: spotify:album:4aawyAB9vmqN3uQ7FjRGTy
            artists:
            - name: Pitbull
              uri: spotify:artist:0TnOYISbd1XYRBk9myaseg
            tracks:
            - artists:
              - artists:
                - name: Pitbull
                  uri: spotify:artist:0TnOYISbd1XYRBk9myaseg
                - name: Sensato
                  uri: spotify:artist:7iJrDbKM5fEkGdm5kpjFzS
              track: Global Warming
              uri: spotify:track:6OmhkSOpvYBokMKQxpIGx2
  type: dict

output:
  description: "returns a dict with all tracks from one album in long output format"
  returned: on success
  sample:
    changed: True
    result:
        href: https://api.spotify.com/v1/albums/4aawyAB9vmqN3uQ7FjRGTy/tracks?offset=0&limit=50
            items:
            - artists:
              - external_urls:
                  spotify: https://open.spotify.com/artist/0TnOYISbd1XYRBk9myaseg
                href: https://api.spotify.com/v1/artists/0TnOYISbd1XYRBk9myaseg
                id: 0TnOYISbd1XYRBk9myaseg
                name: Pitbull
                type: artist
                uri: spotify:artist:0TnOYISbd1XYRBk9myaseg
              - external_urls:
                  spotify: https://open.spotify.com/artist/7iJrDbKM5fEkGdm5kpjFzS
                href: https://api.spotify.com/v1/artists/7iJrDbKM5fEkGdm5kpjFzS
                id: 7iJrDbKM5fEkGdm5kpjFzS
                name: Sensato
                type: artist
                uri: spotify:artist:7iJrDbKM5fEkGdm5kpjFzS
              available_markets: []
              disc_number: 1
              duration_ms: 85400
              explicit: true
              external_urls:
                spotify: https://open.spotify.com/track/6OmhkSOpvYBokMKQxpIGx2
              href: https://api.spotify.com/v1/tracks/6OmhkSOpvYBokMKQxpIGx2
              id: 6OmhkSOpvYBokMKQxpIGx2
              is_local: false
              name: Global Warming
              preview_url: null
              track_number: 1
              type: track
              uri: spotify:track:6OmhkSOpvYBokMKQxpIGx2
            [...]
          limit: 50
          next: null
          offset: 0
          previous: null
          total: 18
  type: dict

output:
  description: "returns a dict with all tracks from one album in long output format"
  returned: on success
  sample:
    changed: True
    result:
        tracks:
            - artists:
              - artists:
                - name: Pitbull
                  uri: spotify:artist:0TnOYISbd1XYRBk9myaseg
                - name: Sensato
                  uri: spotify:artist:7iJrDbKM5fEkGdm5kpjFzS
              track: Global Warming
              uri: spotify:track:6OmhkSOpvYBokMKQxpIGx2
  type: dict
  ```
