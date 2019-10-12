import applescript
import time
from shutil import copy
import numpy as np
import pickle

with open("itunesutils.applescript") as f:
    script_file = f.read()

SCRIPT = applescript.AppleScript(script_file)

def get_metadata(pid):
    meta_map = {
        'ID  ': 'id',
        'pidx': 'index',
        'pnam': 'name',
        'pPIS': 'persistent_id',
        'pDID': 'database_id',
        'pAdd': 'date_added',
        'pTim': 'time',
        'pDur': 'duration',
        'pArt': 'artist',
        'pAlA': 'album_artist',
        'pCmp': 'composer',
        'pAlb': 'album',
        'pGen': 'genre',
        'pBRt': 'bit_rate',
        'pSRt': 'sample_rate',
        'pTrC': 'track_count',
        'pTrN': 'track_number',
        'pDsC': 'disc_count',
        'pDsN': 'disc_number',
        'pSiz': 'size',
        'pAdj': 'volume_adjustment',
        'pYr ': 'year',
        'pCmt': 'comment',
        'pEQp': 'eq',
        'pKnd': 'kind',
        'pMdK': 'media_kind',
        'pVdK': 'video_kind',
        'asmo': 'modification_date',
        'enbl': 'enabled',
        'pStr': 'start',
        'pStp': 'finish',
        'pPlC': 'played_count',
        'pSkC': 'skipped_count',
        'pAnt': 'compilation',
        'pRte': 'rating',
        'pBPM': 'bpm',
        'pGrp': 'grouping',
        'pBkm': 'bookmarkable',
        'pBkt': 'bookmark',
        'pSfa': 'shufflable',
        'pLyr': 'lyrics',
        'pCat': 'category',
        'pDes': 'description',
        'pShw': 'show',
        'pSeN': 'season_number',
        'pEpD': 'episode_id',
        'pEpN': 'episode_number',
        'pUnp': 'unplayed',
        'pSNm': 'sort_name',
        'pSAl': 'sort_album',
        'pSAr': 'sort_artist',
        'pSCm': 'sort_composer',
        'pSAA': 'sort_album_artist',
        'pSSN': 'sort_show',
        'pLov': 'loved',
        'pHat': 'disliked',
        'pALv': 'album_loved',
        'pAHt': 'album_disliked',
        'pClS': 'cloud_status',
        'pWrk': 'work',
        'pMNm': 'movement',
        'pMvN': 'movement_number',
        'pMvC': 'movement_count',
        'pLoc': 'location',
        'pcls': 'class'
    }
    meta_raw = SCRIPT.call('getMetaData', pid)
    meta = {meta_map[k.code.decode()]: v for k,v in meta_raw.items()}
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
        if isinstance(track['play_count'], int):
            script.call("updatePlaycount", track['persistent_id'], track['play_count'])
        if track['skip_count'] is not NaN:
            script.call("updateSkipcount", track['persistent_id'], track['skip_count'])
        if track['genre'] is not NaN:
            script.call("updateGenre", track['persistent_id'], track['genre'])

    time = data2.date_added.dt.total_seconds
    # Set the system clock
    time.clock_settime(time.CLOCK_REALTIME, time)

    # TODO: create an applescript to remove and add the file

    script = applescript.AppleScript("""
        on updatePlaycount(pId, newPlaycount)
            tell application "iTunes"
                set theSong to (the first track whose persistent ID is pId)
                tell theSong
                    set played count to newPlaycount
                end tell
            end tell
        end updatePlaycount

        on updateSkipcount(pId, newSkipcount)
            tell application "iTunes"
    	       set theSong to (the first track whose persistent ID is pId)
    	       tell theSong
    		         set skipped count to newSkipcount
    	       end tell
            end tell
        end updateSkipcount

        on updateGenre(pId, newGenre)
            tell application "iTunes"
    	       set theSong to (the first track whose persistent ID is pId)
    	       tell theSong
    		         set genre to newGenre
    	       end tell
            end tell
        end updateGenre

        on updateDateAdded(pId, newDateAdded)
            tell application "iTunes"
                set theSong to (the first track whose persistent ID is pId)
                tell theSong
                    set date added to newDateAdded
                end tell
            end tell
        end updateDateAdded
    """)

    master_changes_df = pickle.load(open("../data/master_changes.p", "rb"))
    master_changes = master_changes_df.to_dict("records")

    test = {
        'persistent_id': 'B7255BC0871625AA',
        'genre': 'Mashup',
        'play_count': 97.0,
        'skip_count': 9.0,
        'date_added': pd.Timestamp('2011-08-17 17:04:00'),
        'artist': 'The White Panda',
        'name': 'Good For Girls',
        'album': 'www.thewhitepanda.com',
        'date_added_secs': 1313600640.0
    }

    for track in master_changes:
        if track['play_count'] is not NaN:
            script.call("updatePlaycount", track['persistent_id'], track['play_count'])
        if track['skip_count'] is not NaN:
            script.call("updateSkipcount", track['persistent_id'], track['skip_count'])
        if track['genre'] is not NaN:
            script.call("updateGenre", track['persistent_id'], track['genre'])
        # TODO: Logging

    for track in master_changes:
        if track['date_added_secs'] is not None:
            path = helpers.call('getFilePath', track['persistent_id'])
            new_path = '/Users/AB/Desktop/itunesutils_tmp/'
            copy(path, new_path)
            # TODO: does deleting it this way remove the file from iTunes media?
            # TODO: Do I need to purge the itunesutils_tmp folder?
            metadata = helpers.call('getMetaData', track['persistent_id'])
            # TODO
            playlists = helpers.call('getPlaylists', track['persistent_id'])
            helpers.call('deleteTrack', track['persistent_id'])
            time.clock_settime(time.CLOCK_REALTIME, track['date_added_secs'])
            helpers.call('addFile', new_path)
            # TODO:
            # get the new PID and update metadata

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
    helpers = applescript.AppleScript("""
        on getFilePath(pId)
        	tell application "iTunes"
        		set theTrack to (the first track whose persistent ID is pId)
        		try
        			set thePath to POSIX path of (get location of theTrack)
        		on error
        			set thePath to "ERROR: Not playing from local library."
        		end try
        	end tell
        end getFilePath

        on addFile(path)
            set theFile to POSIX file path
            tell application "iTunes" to add theFile
            -- get the persistent ID of theFile
        end addFile

        on getMetaData(pId)
            tell application "iTunes"
        	   set theTrack to the first track whose persistent ID is pId
        	   get properties of theTrack
            end tell
        end getMetaData

        on getPlaylists

        end getPlaylists

        on deleteTrack(pId)
            tell application "iTunes"
                delete (the first track whose persistent ID is pId)
            end tell
        end deleteTrack
    """)



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
