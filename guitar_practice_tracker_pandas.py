import pandas as pd
from datetime import date


path = "P:\\"
filename = "guitar_practice_tracker.xlsx"

topics = {
    "Music_Theory": 0,
    "Sight Reading": 0,
    "Ear Training": 0,
    "FretBoard Mastery": 0,
    "Work on Scales": 0,
    "Work on Chords": 0,
    "Arpeggios": 0,
    "Legato": 0,
    "Vibrato": 0,
    "Slide": 0,
    "Bends": 0,
    # "Improvisation": 0,
    # "Song Practice": 0,
    # "Flamenco RH": 0,
    # "Flamenco LH": 0,
    # "Tremelo": 0,
    # "Sweep Picking": 0,
    # "Hybrid Picking": 0,
    # "Tapping": 0,
    # "Natural Harmonics": 0,
    # "Artificial Harmonics": 0,
    # "Percussive": 0,
    # "Whammy bar" : 0,
    # "Pedals" : 0,
  }


try:
  # check if an excel file is available
  df = pd.read_excel(path + filename, index_col=0)
  print("Found existing database")

except Exception as e:
  # if unavailable create a dataframe, to be later exported as exce;
  print(e)
  print("Existing database not found. Creating a new database (dataframe)\n")

  df = pd.DataFrame(topics,
                    index=pd.date_range(start="06-03-2021", periods=1, freq="D"))


# get date for the index column of the dateframe for the new inputs
def get_date():
  """
  Retrieve custom or current date in the appropriate format
  :return: None
  """

  while True:
    custom_date = input("If the entry is for a custom date, enter after typing date in dd-mm-yyyy; else press ENTER : ")
    if not custom_date:
      return date.today()
    else:
      try:
        return pd.to_datetime(custom_date, format="%d-%m-%Y")
      except:
        print("Wrong Input!!! Either press plain enter key, or provide date in dd-mm-yyyy format. Try again!")


# store date in the update_date variable
update_date = get_date()

# get values to be inputted in the dataframe
def get_minutes(key: str):
  """
  get, authenticate and return input value in minutes

  :param : str | key in a dict
  :return: int | minutes
  """

  bad_input = True
  while bad_input:
    try:
      value = int(input(f"Type minutes spend on {key} today : "))
      if isinstance(value, int) and value < 60 * 8:  # less than 8 hours of practice
        bad_input = False
        print()
      else:
        print("Bad input received. Input a (whole) number less than 480... Try again!!!")

    except ValueError as e:
      # print(e)
      print("Minutes entered must be a whole number. Try again!!!")
  return value


def get_data_points(data_dict: dict):
  """

  :param data_dict: dict | dictionary of topics and values
  :return: dict | updates in dictionary dtype
  """

  updates_to_add = dict()

  for key in data_dict.keys():
    value = get_minutes(key)
    updates_to_add[key] = value

  return updates_to_add


# get a dictionary of key, value updates
updates = get_data_points(topics)

# update the dataframe
df = df.append(pd.Series(updates,
                         name=update_date),
               ignore_index=False)

print(df.T)

# export df as excel doc with the same file name
df.to_excel(path + filename, index=True)