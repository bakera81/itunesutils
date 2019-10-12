import applescript
import time
from shutil import copy
import numpy as np
import pickle

from meta_cols import META_COLS

with open("itunesutils.applescript") as f:
    script_file = f.read()

SCRIPT = applescript.AppleScript(script_file)

def get_metadata(pid):
    meta_raw = SCRIPT.call('getMetaData', pid)
    meta = {META_COLS[k.code.decode()]: v for k,v in meta_raw.items()}
    meta = {}
    for k,v in meta_raw.items():
        val = v
        if val == '':
            val = None
        # TODO: use inheritance instead
        if "applescript.aecodecs" in str(type(val)):
            val = val.code.decode()
        meta[meta_map[k.code.decode()]] = val

    return meta


if __name__ == "main":
    master_changes_df = pickle.load(open("../data/master_changes.p", "rb"))
    master_changes = master_changes_df.to_dict("records")

    for track in master_changes:
        # TODO: Make sure we handle NaNs
        # TODO: Logging
        if isinstance(track['play_count'], int):
            SCRIPT.call("updatePlaycount", track['persistent_id'], track['play_count'])
        if track['skip_count'] is not NaN:
            SCRIPT.call("updateSkipcount", track['persistent_id'], track['skip_count'])
        if track['genre'] is not NaN:
            SCRIPT.call("updateGenre", track['persistent_id'], track['genre'])

    for track in master_changes:
        # TODO: Make sure we handle missing values properly
        if track['date_added_secs'] is not None:
            if track_cloud_status != "cloud":
                # If local file, delete and re-add
                path = SCRIPT.call('getFilePath', track['persistent_id'])
                new_path = '/Users/AB/Desktop/itunesutils_tmp/'
                copy(path, new_path)
                metadata = get_metadata(track['persistent_id'])
                playlists = SCRIPT.call('getPlaylists', track['persistent_id'])
                # TODO: does deleting it this way remove the file from iTunes media?
                # TODO: Do I need to purge the itunesutils_tmp folder?
                SCRIPT.call('deleteTrack', track['persistent_id'])
                time.clock_settime(time.CLOCK_REALTIME, track['date_added_secs'])
                new_pid = SCRIPT.call('addFile', new_path)

                # Transfer all metadata from the file just deleted to the new one
                if metadata.get('genre'):
                    SCRIPT.call("updateGenre", new_pid, metadata.get('genre'))
                if metadata.get('played_count'):
                    SCRIPT.call("updatePlaycount", new_pid, metadata.get('played_count'))
                if metadata.get('skipped_count'):
                    SCRIPT.call("updateSkipcount", new_pid, metadata.get('skipped_count'))
                if metadata.get('rating'):
                    # TODO
                    SCRIPT.call("updateRating", new_pid, metadata.get('rating'))
                if metadata.get('loved'):
                    # TODO
                    SCRIPT.call("updateLoved", new_pid, metadata.get('loved'))

                if len(playlists) != 0:
                    # TODO
                    SCRIPT.call("addToPlaylists", new_pid, playlists)
            else:
                # We are dealing with Apple Music


    # To update the date:
    # 1. DONE Return the path of the file
    # 2. DONE Copy the file to ~/Desktop/itunesutils_tmp
    # 3. DONE Return all metadata for the track (pId, playlists, rating, loved)
    # 4. DONE Delete the song
    # 5. DONE Get new metadata from spreadsheet
    # 6. DONE Turn back the clock
    # 7. DONE Add the song
    # 8. Add the song to all playlists, update metadata
    # NOTE: genre, skipcount, and playcount will need to be updated before the pID changes
    #### Note: pId does not remain the same. We will need to remap the pID



    # Steps 1-2
    path = helpers.call('getFilePath', '9650D59787154E54')
    copy(path, '/Users/AB/Desktop/itunesutils_tmp/')

    #print(script.call('updateGenre', '9650D59787154E54', 'yah bish'))

    # Step 3
    meta_raw = helpers.call('getMetaData', '9650D59787154E54')
    meta = {k.code.decode(): v for k,v in meta_raw.items()}

    # Step 5
    master_changes_df = pickle.load(open("../data/master_changes.p", "rb"))
    master_changes = master_changes_df.to_dict("records")
    # Note: beware of nans and NaTs
    # master_changes[-500]

    # Step 6
    # Change it back to current time by checking "Set date and time automatically" system preferences.
    # May need sudo
    time.clock_settime(time.CLOCK_REALTIME, test['date_added_secs'])
