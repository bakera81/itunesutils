
import applescript

script = applescript.AppleScript("""
    on updateDateAdded(pId, newDateAdded)
        tell application "iTunes"
            set theSong to (the first track whose persistent ID is pId)
            tell theSong
                set date added to newDateAdded
            end tell
        end tell
    end updateDateAdded

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
""")

print(script.call('updateGenre', '9650D59787154E54', 'yah bish'))
