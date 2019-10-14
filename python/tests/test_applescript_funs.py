import applescript
import pytest
import os

from update_metadata import get_metadata

@pytest.fixture
def script():
    with open("itunesutils.applescript") as f:
        script_file = f.read()
    script = applescript.AppleScript(script_file)
    yield script


@pytest.fixture
def pid(script):
    pid = script.call("addFile", "/Users/ab/Repos/itunesutils/python/tests/UFO_Takeoff-Sonidor-1604321570_1.mp3")
    yield pid
    script.call("deleteTrack", pid)


@pytest.fixture
def test_playlist_ids():
    return [75760, 75763]

# GETTERS

def test_get_metadata(script, pid):
    meta = get_metadata(pid)

    assert meta.get('persistent_id') == pid
    assert "UFO" in meta.get('name')
    assert meta.get('genre') == "Electronic"


def test_getFilePath(script, pid):
    path = script.call("getFilePath", pid)

    assert os.path.exists(path)
    assert ("iTunes" in path)


def test_getPlaylists(script, pid, test_playlist_ids):
    playlists = script.call("getPlaylists", pid)
    assert isinstance(playlists, list) and (len(playlists) == 0)

    script.call("addToPlaylists", pid, test_playlist_ids)
    playlists = script.call("getPlaylists", pid)
    assert playlists == test_playlist_ids


@pytest.mark.skip
def test_getPIdFromSelection():
    # No need to test
    pass

# SETTERS

def test_setPlayCount(script, pid):
    script.call("setPlayCount", pid, 42)
    track = get_metadata(pid)

    assert track.get('played_count') == 42


def test_setSkipCount(script, pid):
    script.call("setSkipCount", pid, 42)
    track = get_metadata(pid)

    assert track.get('skipped_count') == 42


def test_setGenre(script, pid):
    script.call("setGenre", pid, "ohhh yeaaahhh")
    track = get_metadata(pid)

    assert track.get('genre') == "ohhh yeaaahhh"


def test_setRating(script, pid):
    script.call("setRating", pid, 1)
    track = get_metadata(pid)

    assert track.get("rating") == 1


def test_setLoved(script, pid):
    script.call("setLoved", pid, True)
    track = get_metadata(pid)

    assert track.get("loved") == True


# ACTIONS

def test_addToPlaylists(script, pid, test_playlist_ids):
    script.call("addToPlaylists", pid, test_playlist_ids)
    playlists = script.call("getPlaylists", pid)

    assert playlists == test_playlist_ids


@pytest.mark.skip
def test_addFile():
    # Used in fixture
    pass


@pytest.mark.skip
def test_deleteTrack(script, pid):
    # Used in fixture
    pass
