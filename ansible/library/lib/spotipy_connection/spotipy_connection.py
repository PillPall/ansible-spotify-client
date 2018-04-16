# Spotipy Connection helper

import sys
import yaml
import os
import spotipy

def client(module):
    auth_token = module.params.get("auth_token")

    try:
        return spotipy.Spotify(auth=auth_token)
    except Exception as e:
        module.fail_json(msg="Error: Can't get token - " + str(e))

def create_config(module):
    if module.params.get("config_file"):
        created_config = read_config(module.params.get("config_file"))
    elif module.params.get("client_id") and module.params.get("client_secret"):
        client_id = module.params.get("client_id")
        client_secret = module.params.get("client_secret")
        created_config = build_config(module, client_id, client_secret)
    elif os.getenv('SPOTIPY_CLIENT_ID') and os.getenv('SPOTIPY_CLIENT_SECRET'):
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        created_config = build_config(module, client_id, client_secret)
    else:
        module.fail_json(msg="Error: Can't find credentials")

    return created_config

def build_config(module, client_id, client_secret):
    conf = {}
    conf.update({'client_id': client_id})
    conf.update({'client_secret': client_secret})
    if module.params.get("username"):
            conf.update({'username': module.params.get("username")})
            conf.update({'redirect_uri': module.params.get("redirect_uri")})
            conf.update({'scope': module.params.get("scope")})

    return conf

def read_config(config_file):
    with open(config_file, 'r') as ymlfile:
        conf = yaml.load(ymlfile)

    return conf

def sp_search(client, q, limit=10, offset=0, type='artist', market=None):
    if type is 'artist':
        return client.search(q=q, limit=limit, offset=offset, type=type, market=market)
    elif type is 'album':
        return client.search(q=q, limit=limit, offset=offset, type=type, market=market)
    elif type is 'playlist':
        return client.search(q=q, limit=limit, offset=offset, type=type, market=market)
    elif type is 'track':
        return client.search(q=q, limit=limit, offset=offset, type=type, market=market)
    elif type is 'artists_and_album':
        return client.search(q=q, limit=limit, offset=offset, type='artist,album', market=market)
    elif type is 'artists_and_tracks':
        return client.search(q=q, limit=limit, offset=offset, type='artist,track', market=market)
