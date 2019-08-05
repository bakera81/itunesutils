import pickle
import pandas as pd
from datetime import datetime
from libpytunes import Library
form time import mktime
import os
from siuba import join

base_path = "/Users/AB/Documents/itunesutils"
old_lib_path = "data/2016-07-15/Library.xml"
old_pickle_file = "data/2016-07-15/itl.p"
new_lib_path = "data/2019-07-31/Library.xml"
new_pickle_file = "data/2019-07-31/itl.p"

itl_source = Library(old_lib_path)
pickle.dump(itl_source, open(old_pickle_file, "wb"))

itl_source = Library(new_lib_path)
pickle.dump(itl_source, open(new_pickle_file, "wb"))

itl = pickle.load(open(old_pickle_file, "rb"))
songs_data = [s[1].ToDict() for s in itl.songs.items()]
songs_1 = pd.DataFrame(songs_data)

itl = pickle.load(open(new_pickle_file, "rb"))
songs_data = [s[1].ToDict() for s in itl.songs.items()]
songs_2 = pd.DataFrame(songs_data)

# correct datetimes
songs_2 = songs_2 >> \
    mutate(date_added = lambda: _.date_added. datetime.fromtimestamp(mktime(date_added)))

convert_time = lambda x: datetime.fromtimestamp(mktime(x))
songs_2.date_added.apply(convert_time).astype("datetime64[ns]")


summarize(songs_2, max_date_added = _.date_added.max())
