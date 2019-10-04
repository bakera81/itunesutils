
import applescript
import time
from shutil import copy

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

# To update the date:
# 1. DONE Return the path of the file
# 2. DONE Copy the file to ~/Desktop/itunesutils_tmp
# 3. DONE Return all metadata for the track (pId, playlists, rating, loved)
# 4. DONE Delete the song
# 5. Get new metadata from spreadsheet
# 6. Turn back the clock
# 7. DONE Add the song
# 8. Add the song to all playlists, update metadata
#### Note: pId does not remain the same. We will need to remap the pID
helper_script = applescript.AppleScript("""
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
    end addFile

    on getMetaData(pId)
        tell application "iTunes"
    	   set theTrack to the first track whose persistent ID is pId
    	   get properties of theTrack
        end tell
    end getMetaData

    on deleteTrack(pId)
        tell application "iTunes"
            delete (the first track whose persistent ID is "BE03E03F897BBBCE")
        end tell
    end deleteTrack
""")



# Steps 1-2
path = date_script.call('getFilePath', '9650D59787154E54')
copy(path, '/Users/AB/Desktop/itunesutils_tmp/')

#print(script.call('updateGenre', '9650D59787154E54', 'yah bish'))

# Step 3
meta_raw = date_script.call('getMetaData', '9650D59787154E54')
meta = {k.code.decode(): v for k,v in meta_raw.items()}


# tell application "iTunes"
# 	set theTrack to item 1 of (get selection)
# 	get persistent ID of theTrack
# end tell
