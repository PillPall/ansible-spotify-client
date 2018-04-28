# Spotify artists top tracks

#### Modules
spotify_artists_top_tracks - Ansible module to get top tracks for artists

* Synopsis
* Options
* Examples
* Return value

#### Synopsis

Ansible module to get the top tracks for an artists in a specific country. Artists can be provided via **name, URI or JSON File**. A JSON file can be generated using the Ansible module `spotify_search` or `spotify_related_artists` or visit this site for more informations [Link](https://beta.developer.spotify.com/documentation/web-api/reference/artists/get-artist/).

You can only define one of the options at the same time: `artists_name`, `artists_file` or `artists_uri`.

The options `country_code`, `dest_file` and `output_format` can be combined with all other options.

#### Options

| Parameter     | type        |required    | default  | choices  | comments |
| ------------- |-------------| ---------|----------- |--------- | -------- |
| auth_token    | String       | Yes    | null       | null     |  Authentication token for Spotify API. Taken from the module spotify_auth |
| artists_file  | String       | No     | null       | null     | JSON File containing a dict of track names.|
| artists_name  | String       | No     | null       | null     | Artists name to get the related artists for. |
| artists_uri   | String       | No     | null       | null     |  Artists URI to get top tracks for. |
| country_code  | String       | No     | AU         | null     |  Artists URI to get top tracks for. |
| dest_file     | String       | No     | null       | null     |  Destination file to save the output to. |
| output_format  | String      | No     | long       | short, long |  Control Ansible output format. |

#### Requirements  
* python >= 2.7.10
* spotipy >= 2.4.4

#### Examples
```
- name: Get top tracks for an named artist in australia and save it to file
  spotify_artists_top_tracks:
    auth_token: 0123456789ABCDEFGHI
    artist_name: young the giant
    country_code: au
    dest_file: artists.json
    output_format: short

- name: Get top tracks for an artists with given URI wi in germany
  spotify_artists_top_tracks:
    auth_token: 0123456789ABCDEFGHI
    artists_uri: spotify:artist:4j56EQDQu5XnL7R3E9iFJT
    country_code: de
    output_format: long
  register: results

- name: Get top tracks for artists via file
  spotify_artists_top_tracks:
    auth_token: 0123456789ABCDEFGHI
    artists_file: "{{ playbook_dir }}/files/related_artists.json"
    output_format: long
  register: results

- name: Example of how to get top tracks for artists found with Ansible module spotify_related_artists
  spotify_related_artists:
    auth_token: 0123456789001234567890ABCDEFGHIJK
    artists_name: "Young the Giant"
    dest_file: "{{ playbook_dir }}/files/related_artists.json"

  spotify_artists_top_tracks:
    auth_token: 0123456789ABCDEFGHI
    artists_file: "{{ playbook_dir }}/files/related_artists.json"
    output_format: long
    dest_file: "{{ playbook_dir }}/files/related_artists_top_tracks.json"
```
#### RETURN VALUES:

```  
description: "returns a dict type with defined output_format short."
  returned: on success
  sample:
    changed: True
    result:
        tracks:
            track: Cough Syrup
            uri:spotify:track:4Tfe8Uu9faFdWRiZbpvpXd
  type: dict

  description: "returns a dict type with undefined or defined output_format long."
    returned: on success
    sample:
      changed: True
      result:
        tracks:
        - album:
            album_type: album
            name: The English Riviera
            external_urls:
              spotify: https://open.spotify.com/album/716fnrS2qXChPC3J2X73pK
            release_date: '2011-04-11'
            uri: spotify:album:716fnrS2qXChPC3J2X73pK
            href: https://api.spotify.com/v1/albums/716fnrS2qXChPC3J2X73pK
            artists:
            - name: Metronomy
              external_urls:
                spotify: https://open.spotify.com/artist/54QMjE4toDfiCryzYWCpXX
              uri: spotify:artist:54QMjE4toDfiCryzYWCpXX
              href: https://api.spotify.com/v1/artists/54QMjE4toDfiCryzYWCpXX
              type: artist
              id: 54QMjE4toDfiCryzYWCpXX
            images:
            - url: https://i.scdn.co/image/58c589a54b0be1c12732f6b929522fd1e74a988e
              width: 640
              height: 640
            - url: https://i.scdn.co/image/6be6bddab8cfcfb4a721e2fa8ecde41bd05db44b
              width: 300
              height: 300
            - url: https://i.scdn.co/image/2b86a04a2dfef6d8770a2ced40eb58aaa51eb87c
              width: 64
              height: 64
            type: album
            id: 716fnrS2qXChPC3J2X73pK
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
            release_date_precision: day
          is_local: false
          name: The Look
          uri: spotify:track:6zfczP87XO2SxWlQtnjFNa
          external_urls:
            spotify: https://open.spotify.com/track/6zfczP87XO2SxWlQtnjFNa
          popularity: 69
          explicit: false
          preview_url: https://p.scdn.co/mp3-preview/45199068ba52d3414be397ff0e149ca290fe64d4?cid=550ccd7bc5504fa29542d26bc1848822
          track_number: 4
          disc_number: 1
          href: https://api.spotify.com/v1/tracks/6zfczP87XO2SxWlQtnjFNa
          artists:
          - name: Metronomy
            external_urls:
              spotify: https://open.spotify.com/artist/54QMjE4toDfiCryzYWCpXX
            uri: spotify:artist:54QMjE4toDfiCryzYWCpXX
            href: https://api.spotify.com/v1/artists/54QMjE4toDfiCryzYWCpXX
            type: artist
            id: 54QMjE4toDfiCryzYWCpXX
          duration_ms: 277653
          external_ids:
            isrc: GBMVH1100040
          type: track
          id: 6zfczP87XO2SxWlQtnjFNa
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

    type: dict

  ```
