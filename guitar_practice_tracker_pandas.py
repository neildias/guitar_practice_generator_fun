import pandas as pd
from utils import (get_date, get_file_path, get_data_points,
                   read_create_database_object)


# hardcoded topic heads
topics = {
    "Music_Theory": 0,
    "Sight Reading": 0,
    "Ear Training": 0,
    "Sight Playing (Classical)": 0,
    "FretBoard Mastery": 0,
    "Work on Scales": 0,
    "Work on Chords": 0,
    "Arpeggios": 0,
    "Legato": 0,
    "Vibrato": 0,
    "Slide": 0,
    "Bends": 0,
    "Picado": 0,
    "Rasgeo": 0,
    "Pulgar": 0,
    "Alzapua": 0,
    "Golpe": 0,
    "Solea": 0,
    "Alegrias": 0,
    "Tangos": 0,
    "Seguiriya": 0,
    "Tarantas": 0,
    "Granainas": 0,
    "Bulerias": 0,
    "Improvisation": 0,
    "Guitar Licks": 0,
    "Song Practice": 0,
    "Flamenco RH": 0,
    "Flamenco LH": 0,
    "Tremelo": 0,
    "Sweep Picking": 0,
    "Hybrid Picking": 0,
    "Tapping": 0,
    "Natural Harmonics": 0,
    "Artificial Harmonics": 0,
    "Harp Harmonics": 0,
    "Slap Harmonics:": 0,
    "Percussive": 0,
    "Whammy bar": 0,
    "Pedals": 0,
  }

# hardcoded path
path = "P:\\"
filename = "guitar_practice_tracker.xlsx"

# get new_path, filename if the user chooses
new_path, new_filename, new_topic_dict = get_file_path(path, filename, topics)

path = new_path if new_path else path
filename = new_filename if new_filename else filename
topics = new_topic_dict if new_topic_dict else topics

# get data
df = read_create_database_object(path, filename, topics)

# store date in the update_date variable
update_date = get_date()

# get a dictionary of key, value updates
updates = get_data_points(topics)

# update the dataframe
df = df.append(pd.Series(updates,
                         name=update_date),
               ignore_index=False)

print(df.T)

# export df as excel doc with the same file name
df.fillna(0).to_excel(path + filename, index=True)
