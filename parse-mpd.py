"""
    Lee data/mpd/*.json
     Y escribe en data/mpd/reduced/*.json
     Los 1000 archivos habiendo tirado todo menos las uris y encodeando todo
     Funciona secuencial y con globales

"""

import os
import json
import pandas as pd
BASEPATH='data/mpd/'

COUNTERS = {'track': 0,
            'album': 0,
            'artist' : 0
           }
MAPS = {'track': {},
       'album': {},
       'artist': {}
       }

TRACK_INFO = {}

def reduce_playlist(playlist):
    global MAPS, COUNTERS, TRACK_INFO
    res = {}
    res['name'] = playlist['name']
    res['pid'] = playlist['pid']
    res['tracks'] = []
    for t in playlist['tracks']:
        track = {}
        data = {}
        for e in ['album', 'artist', 'track']:
            key = t['{}_uri'.format(e)].replace("spotify:{}:".format(e), "")
            data[e] = key
            if key in MAPS[e]:
                value = MAPS[e][key][0]
            else:
                value = COUNTERS[e]
                COUNTERS[e]+=1
                MAPS[e][key] = (value, t['{}_name'.format(e)])
            if e == 'track':
                track['{}_uri'.format(e)] = value
                if key not in TRACK_INFO:
                    TRACK_INFO[key] = (data['album'], data['artist'])
                
        res['tracks'].append(track['track_uri'])
    return res

def run():
    files = [(i, f, BASEPATH + f) for i, f in enumerate(os.listdir(BASEPATH)) if f.endswith(".json")]
    print(len(files))

    for index, basename, fullpath in files:
        print("Processing {} ({})".format(index, basename))
        playlists = json.load(open(fullpath))['playlists']
        reduced_playlists =  [reduce_playlist(pl) for pl in playlists]
        json.dump(reduced_playlists, open(BASEPATH+"reduced/{}".format(basename), "w"))
    
    json.dump(MAPS, open(BASEPATH+"reduced/maps.json", "w"))
    json.dump(TRACK_INFO, open(BASEPATH+"reduced/track_info.json", "w"))
    
if __name__ == '__main__':
    run()

    

