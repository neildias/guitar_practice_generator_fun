# A useful script when the practice session is over and one needs to
# manually input minutes practices for each practice head
# preset_sched_practice_manager.py and sessions_practice_managers.py are
# more useful script for real time program guided practice.

import pandas as pd
from utils import practice_headers, utils

# hardcoded topic heads
topics = practice_headers.topics

# hardcoded path
path = practice_headers.path
filename = practice_headers.filename

# get new_path, filename if the user chooses
new_path, new_filename, new_topic_dict = utils.get_file_path(path,
                                                             filename,
                                                             topics)

path = new_path if new_path else path
filename = new_filename+".xlsx" if new_filename else filename
topics = new_topic_dict if new_topic_dict else topics

# get data
df = utils.read_create_database_object(path, filename, topics)

# store date in the update_date variable
update_date = utils.get_date()
print()

# get a dictionary of key, value updates
updates = utils.get_data_points(topics)

# update the dataframe
df = df.append(pd.Series(updates,
                         name=update_date),
               ignore_index=False)


print(df.T)

# ensure Total Mins is Last col
position = len(df.columns) - 1
df = utils.column_reorder(df, "Total Mins", position)

# export df as excel doc with the same file name
df.fillna(0).to_excel(path + filename, index=True)
