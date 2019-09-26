
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
# 1. Return the path of the file
# 2. Copy the file to ~/Desktop/itunesutils_tmp
# 3. Return all metadata for the track (playlists, rating, loved)
# 4. Delete the song
#### TODO: does the pId remain the same? we need to be able to update the other metadata too
# 5. Get new metadata from spreadsheet
# 6. Turn back the clock
# 7. DONE Add the song
# 8. Add the song to all playlists, update metadata
date_script = applescript.AppleScript("""
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
""")


path = date_script.call('getFilePath', '9650D59787154E54')

copy(path, '/Users/AB/Desktop/itunesutils_tmp/')

print(script.call('updateGenre', '9650D59787154E54', 'yah bish'))
