-- GETTERS

on getMetadata(pId)
	tell application "iTunes"
		set theTrack to the first track whose persistent ID is pId
		get properties of theTrack
	end tell
end getMetadata

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

on getPlaylists(pId)
	tell application "iTunes"
		set theTrack to the first track whose persistent ID is pId
		set currPlaylists to user playlists of theTrack
		set thePlaylistIds to {}
		repeat with currPlaylist in currPlaylists
			-- Add it to the final list only if it isn't already included
			if thePlaylistIds does not contain id of currPlaylist then
				-- Do not include smart playlists
				if currPlaylist is not smart then
					-- set end of thePlaylists to currPlaylist
					set end of thePlaylistIds to id of currPlaylist
				end if
			end if
		end repeat
		get thePlaylistIds
	end tell
end getPlaylists

on getPIdFromSelection()
	tell application "iTunes"
		set theTrack to item 1 of (get selection)
		get persistent ID of theTrack
	end tell
end getPIdFromSelection

-- SETTERS

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

-- ACTIONS

on addFile(file_path)
	set theFile to file_path
	tell application "iTunes"
		set theId to the id of (add theFile)
		set theTrack to the first track whose id is theId
		get the persistent ID of theTrack
	end tell
end addFile

on deleteTrack(pId)
	tell application "iTunes"
		delete (the first track whose persistent ID is pId)
	end tell
end deleteTrack
