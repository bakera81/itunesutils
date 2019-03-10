import pickle
import pandas as pd
from datetime import datetime
from libpytunes import Library


lib_path = "Library.xml"
pickle_file = "itl.p"

# Parse XML
itl_source = Library(lib_path)
pickle.dump(itl_source, open(pickle_file, "wb"))

itl = pickle.load(open(pickle_file, "rb"))


songs_data = [s[1].ToDict() for s in itl.songs.items()]
songs_df = pd.DataFrame(songs_data)

playlist_names = itl.getPlaylistNames() # potentially problematic if names are not distinct
playlists_data = [itl.getPlaylist(p).ToDict() for p in playlist_names]

# "Unnest" the tracks
playlist_songs = []
for playlist in playlists_data:
    skeleton = {k:v for k,v in playlist.items() if k != 'tracks'}

    playlist_songs.extend(
        [{**skeleton, 'tracks': t.track_id} for t in playlist.get('tracks')]
    )
playlists_df = pd.DataFrame(playlist_songs)

# Write CSVs
# TODO: make sure the date columns get parsed properly
songs_df.to_csv('data/{}_songs.csv'.format(
    datetime.today().strftime('%d-%m-%Y')
))

playlists_df.to_csv('data/{}_playlists.csv'.format(
    datetime.today().strftime('%d-%m-%Y')
))
