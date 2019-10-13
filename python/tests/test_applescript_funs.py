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


def test_get_metadata(script, pid):
    meta = get_metadata(pid)

    assert meta.get('persistent_id') == pid
    assert "UFO" in meta.get('name')
    assert meta.get('genre') == "Electronic"


def test_updatePlayCount(script, pid):
    script.call("updatePlayCount", pid, 42)
    track = get_metadata(pid)

    assert track.get('played_count') == 42


def test_updateSkipCount(script, pid):
    script.call("updateSkipCount", pid, 42)
    track = get_metadata(pid)

    assert track.get('skipped_count') == 42


def test_updateGenre(script, pid):
    script.call("updateGenre", pid, "ohhh yeaaahhh")
    track = get_metadata(pid)

    assert track.get('genre') == "ohhh yeaaahhh"


def test_getFilePath(script, pid):
    path = script.call("getFilePath", pid)

    assert os.path.exists(path)
    assert ("iTunes" in path)


@pytest.mark.skip
def test_addFile():
    pass

@pytest.mark.skip
def test_getPlaylists(script, pid):
    playlists = script.call("getPlaylists", pid)
    assert isinstance(playlists, list) and (len(playlists) == 0)

    script.call("addToPlaylists", pid, [playlist_id])
    playlists = script.call("getPlaylists", pid)
    assert playlists == [playlist_id]


@pytest.mark.skip
def test_deleteTrack(script, pid):
    pass
