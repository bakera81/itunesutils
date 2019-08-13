import pandas as pd
import pickle
import datetime
import sys
from nltk.metrics import edit_distance
from siuba import *
from siuba.dply.vector import row_number

needs_to_be_matched = pickle.load(open("../data/manual_cleaning/needs_to_by_joined_wip.p", "rb"))
new_songs = pickle.load(open("../data/data2.p", "rb"))


# needs_to_be_matched = (
#     needs_to_be_matched
#     # Pick up where you left off
#     >> filter(_.persistent_id_y.isna())
# )

# Clean columns used for search
new_songs = new_songs >> mutate(
    artist_clean = _.artist.str.lower(),
    name_clean = _.name.str.lower(),
    album_clean = _.album.str.lower(),
)

def calculate_distance(search):
    return (_
        .dropna()
        .apply(lambda x: edit_distance(x, search))
    )

postprocess = (
    # mutate(choice=row_number(_))
    select(_.artist, _.album, _.name, _.persistent_id)
    >> arrange(_.artist, _.album, _.name)
)

def results_from_standard_search(strict=True):
    print("Searching using substrings...")
    if strict:
        results = (
            new_songs
            >> filter(
                _.artist_clean.str.contains(song.artist.lower(), regex=False),
                _.name_clean.str.contains(song['name'].lower(), regex=False),
            )
        )
    else:
        results = (
            new_songs
            >> filter(
                (_.artist_clean.str.contains(song.artist.lower(), regex=False)) |
                (_.name_clean.str.contains(song['name'].lower(), regex=False)),
            )
        )
    return results >> postprocess


def results_from_artist_search(artist):
    print("Searching using artist...")
    return (
        new_songs
        >> filter(_.artist == artist)
        >> postprocess
    )

def results_from_custom_search(query):
    print("Searching using custom query...")
    return (
        new_songs
        >> filter(
            (_.artist_clean.str.contains(query.lower())) |
            (_.name_clean.str.contains(query.lower())) |
            (_.album_clean.str.contains(query.lower()))
        )
        >> postprocess
    )

def results_from_edit_distance():
    print("Searching using edit distance...")
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
        >> postprocess
    )

    return results

def display_results(results, current_song, i, length=needs_to_be_matched.shape[0]):
    with pd.option_context(
        'display.max_rows', None,
        'display.max_columns', None,
        'display.width', None):
        print(
            results >> select(-_.persistent_id)
        )
    return input("""
        ({0}/{1}) Find a match for:

        song: {2}
        artist: {3}
        album: {4}


        > """.format(
            i,
            length,
            song['name'],
            song.artist,
            song.album
        )
    )

def write_out(df):
    df.to_csv("../data/manual_cleaning/needs_to_by_joined_wip.csv")
    pickle.dump(df, open("../data/manual_cleaning/needs_to_by_joined_wip.p", "wb"))

def match(i, resp):
    # Use the Index rather than the row number
    match = results.loc[int(resp), ]
    needs_to_be_matched.loc[needs_to_be_matched.index[i], "persistent_id_y"] = match.persistent_id
    write_out(needs_to_be_matched)

def increment_reviewed_at(i):
    needs_to_be_matched.loc[needs_to_be_matched.index[i], 'reviewed_at'] = datetime.datetime.now()


nb_pending_review = (
    needs_to_be_matched
    >> filter(_.reviewed_at.isna())
).shape[0]



# Handle complete case
if nb_pending_review == 0:
    print("No work left to do. Congratulations are in order (hopefully).")
    sys.exit()

for i in range(needs_to_be_matched.shape[0]):
    try:
        # Search for matches
        song = needs_to_be_matched.iloc[i]

        # # Skip any song that has already been matched
        # if song.persistent_id_y:
        #     continue

        # Skip any song that has been reviewed
        if song.reviewed_at:
            continue

        # Search using contains
        results = results_from_standard_search(strict=True)

        # Automatically match a song if 1 result
        if results.shape[0] == 1:
            print("""
                Automatically matching:

                {0} => {1}
            """.format(song['name'], results.iloc[0]['name']))
            # import pdb; pdb.set_trace()
            increment_reviewed_at(i)
            match(i, results.index[0])
            continue

        # If no results, loosen the filter
        if results.shape[0] == 0:
            results = results_from_standard_search(strict=False)

        # If still no results, take edit_distance out for a spin
        if results.shape[0] == 0:
            results = results_from_edit_distance()

        # Display results
        resp = display_results(results, song, i)

        valid_cmds = ['m', 'a', 's', 'q', 'c', 'e']

        # Search by default
        if (resp.lower() not in valid_cmds) and (not resp.isnumeric()):
            results = results_from_custom_search(resp)
            resp = display_results(results, song, i)

        if resp.lower() == 'm':
            results = results_from_edit_distance()
            resp = display_results(results, song, i)

        # Do an artist search
        if resp.lower() == 'a':
            results = results_from_artist_search(song.artist)
            resp = display_results(results, song, i)

        # Allow custom search
        if resp.lower() == 's' or resp.lower() == 'q':
            query = input("\t> ")
            results = results_from_custom_search(query)
            resp = display_results(results, song, i)

        if resp.lower() == 'c':
            increment_reviewed_at(i)
            continue

        # If error, make leave entries blank to return to it
        if resp.lower() == 'e':
            continue

        # Future music: Include option to search for just the artist or just the song

        # Update needs_to_be_matched
        print("Great! You chose {}.".format(results.loc[int(resp), "name"]))
        increment_reviewed_at(i)
        match(i, resp)


    # Save file on exit (or anything bad happening)
    except:
        e = sys.exc_info()[0]
        print(e)
        print("\n\nSaving...")
        write_out(needs_to_be_matched)
        print("Goodbye for now, my friend.")
        break
