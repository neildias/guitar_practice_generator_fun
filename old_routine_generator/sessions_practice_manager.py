# Useful for managing live spontaneous, usually shorter practice sessions
# Time is safely stored in an excel file automatically
# User enters the time for each activity, and the program guides the user
# through to the completion of the session

import pandas as pd
from utils import gui_timer, practice_headers, utils, countdown_timer
from tkinter import *

# hardcoded path
path = practice_headers.path
filename = practice_headers.filename
topics = practice_headers.topics

# get new_path, filename if the user chooses
new_path, new_filename, new_topic_dict = utils.get_file_path(path, filename,
                                                             topics)

path = new_path if new_path else path
filename = new_filename+".xlsx" if new_filename else filename
topics = new_topic_dict if new_topic_dict else topics

# get practice heads and timings to practice from user
user_topic_timings = utils.topic_duration_capture(topics)

# run countdown clock over users input
# countdown_timer.countdown_clock(user_topic_timings)
root = Tk()
root.title(f"Practice Countdown for Mastery")
label_object = Label(root,
                     font=('calibri', 50, 'bold'),
                     background="blue",
                     foreground="white")
gui_timer.gui_timer(user_topic_timings, label_object)

# add totals key
user_topic_timings["Total Mins"] = utils.total_dict_values(user_topic_timings)

# get data
df = utils.read_create_database_object(path, filename, user_topic_timings)

# store date in the update_date variable
update_date = utils.get_date()

# get a dictionary of key, value updates
#updates = utilsdfsdf.get_data_points(user_topic_timings)

# update the dataframe
df = df.append(pd.Series(user_topic_timings,
                         name=update_date),
               ignore_index=False)


print(df.T)

# ensure Total Mins is Last col
position = len(df.columns) - 1
df = utils.column_reorder(df, "Total Mins", position)

# export df as excel doc with the same file name
df.fillna(0).to_excel(path + filename, index=True)

mainloop()