import pandas as pd
import pickle
from nltk.metrics import edit_distance
from siuba import *
from siuba.dply.vector import row_number

needs_to_be_matched = pickle.load(open("../data/manual_cleaning/needs_to_by_joined_wip.p", "rb"))
new_songs = pickle.load(open("../data/data2.p", "rb"))


needs_to_be_matched = (
    needs_to_be_matched
    # Pick up where you left off
    >> filter(_.persistent_id_y.isna())
)

# Clean columns used for search
new_songs = new_songs >> mutate(
    artist_clean = _.artist.str.lower(),
    name_clean = _.name.str.lower()
)

def calculate_distance(search):
    return (_
        .dropna()
        .apply(lambda x: edit_distance(x, search))
    )

add_row_number = (
    mutate(choice=row_number(_))
    >> select(_.choice, _.artist, _.album, _.name, _.persistent_id)
)

def results_from_edit_distance():
    artist_distance = calculate_distance(song.artist.lower())
    name_distance = calculate_distance(song['name'].lower())

    results = (
        new_songs
        >> mutate(
            artist_distance=artist_distance(_.artist_clean),
            name_distance=name_distance(_.name_clean),
        )
    )

    results['artist_ntile'] = pd.qcut(results.artist_distance, 20, duplicates='drop')
    results['name_ntile'] = pd.qcut(results.name_distance, 20, duplicates='drop')

    results = (
        results
        >> filter(
            _.artist_ntile == _.artist_ntile.cat.categories[0],
            _.name_ntile == _.name_ntile.cat.categories[0],
        )
        >> add_row_number
    )

    return results

def display_results(results, current_song):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(
            results >> select(-_.persistent_id)
        )
    return input("""
        Find a match for:

        song: {0}
        artist: {1}
        album: {2}


        > """.format(song['name'], song.artist, song.album))

def match(i, resp):
    import pdb; pdb.set_trace()
    match = results.iloc[int(resp) - 1]
    # Confirm this doesn't cause issues (difference between row number and index?)
    # UPDATE: It looks like it is causing issues
    # needs_to_be_matched.at[i, 'persistent_id_y'] = match.persistent_id
    # needs_to_be_matched.insert(i, 'persistent_id_y', match.persistent_id)
    needs_to_be_matched.loc[needs_to_be_matched.index[i], "persistent_id_y"] = match.persistent_id

    needs_to_be_matched.to_csv("../data/manual_cleaning/test.csv")

# Handle complete case

for i in range(needs_to_be_matched.shape[0]):
    # Search for matches
    print("Searching...")
    song = needs_to_be_matched.iloc[i]

    # Search using contains
    results = (
        new_songs
        >> filter(
            _.artist_clean.str.contains(song.artist.lower()),
            _.name_clean.str.contains(song['name'].lower()),
        )
        >> add_row_number
    )

    # Automatically match a song if 1 result
    if results.shape[0] == 1:
        print("""
            Automatically matching:

            {0} => {1}
        """.format(song['name'], results.iloc[0]['name']))
        match(i, 1)
        continue

    # If not, take edit_distance out for a spin
    if results.shape[0] == 0:
        results = results_from_edit_distance()

    # Display results
    resp = display_results(results, song)

    if resp.lower() == 'c':
        continue

    if resp.lower() == 'm':
        results = results_from_edit_distance()
        resp = display_results(results, song)

    # Future music: Include option to search for just the artist or just the song

    # Update needs_to_be_matched
    match(i, resp)


    # Save file on exit
