from utils.default_params import today, note_duration, note_duration_dict
import pandas as pd


def get_int_input(message: str):
  """
  A simple function to get int inputs from the user.

  :param message: str | Message that goes into the prompt
  :return int | int input
  """
  while True:
    try:
      int_input = int(input(message))
      return int_input
    except:
      print("Wrong Input! Please enter a number. ")


# get date for the index column of the dataframe for the new inputs
def get_date():
  """
  Retrieve custom or current date in the appropriate format

  :return: python or pandas date object. Later if user inputs a date
  """

  while True:
    custom_date = input(
      "To input a custom date, enter the same in dd-mm-yyyy;"
      " else press ENTER : "
    )
    if not custom_date:
      return today
    else:
      try:
        return pd.to_datetime(custom_date, format="%d-%m-%Y")
      except ValueError:
        print("Wrong Input!!! Either press plain enter key, or provide date in "
              "dd-mm-yyyy format. Try again!")


def dict_keys_to_str(dictionary: dict):
  """
  Returns a single string of all the keys of the dictionary passed

  :param dictionary: dict
  :return str
  """
  key_list = [key for key in dictionary.keys()]
  return " | ".join(key_list)


def print_keys(dictionary: dict,
               value: bool = True,
               duration: bool =False,
               message: str =""):
  """
  Prints all the keys of the dictionary passed. Note that the duration and the
  message arguments are only used if "value" is set to True

  :param dictionary: dict
  :param value: bool
  :param duration: bool or float
  :param message: str

  """
  for key, value in dictionary.items():
    if value:

      if not duration:
        print(key, value, message)
      elif isinstance(duration, float):
        print(key,
              round(value*duration,2),
              message)
    else:
      print(key)


def get_input_number(message: str,
                     starting: int,
                     ending: int,
                     allow_no_input=False,):
  """
  Asks user for a value, ensures the value inserted is either an int or a float,
  and within the prescribed range

  :param message: str
  :param starting: int starting number
  :param ending: int ending number
  :param allow_no_input: bool | allows no input == ""
  :return int or float
  """
  while True:
    try:
      number = input(message)
      if allow_no_input: # exit if no input received
        if number == "":
          return
      # else try to convert to float
      number = float(number)
      if number >= starting and number <= ending:
        break
      else:
        print(f"\nPlease input a number from {starting} and {ending}, "
              f"inclusive both")
    except:
      print("Invalid input. Please enter a number eg. 1 or 0.5. ")
  return number


def get_data_points(data_dict: dict,
                    only_practiced_items: bool =False):
  """
  Returns a dictionary of totalled values for each header

  :param data_dict: dict | dictionary of topics and values
  :return: dict | updates in dictionary data type
  """

  updates_to_add = dict()
  towards_total_minutes = 0
  for lesson, time in data_dict.items():
    updates_to_add[lesson] = time
    towards_total_minutes += time
    if only_practiced_items:
      # removes values with zero minutes
      if not time:
        del data_dict[lesson]
  updates_to_add["Total Mins"] = towards_total_minutes

  return updates_to_add


def column_reorder(df, col_name, position=None):
  """
  Reorders df columns
  :param df:
  :param col_name:
  :param position:
  :return:
  """
  if position is None:
    position = len(df.columns) - 1
  temp_series = df[col_name]
  df = df.drop(col_name, axis=1)
  df.insert(loc=position, column=col_name, value=temp_series)
  return df


def get_tempo_note_duration():
  """

  :return: str
  """
  # get tempo
  tempo_message = "\n\nPlease enter the LAST tempo used for this practice: "
  tempo = get_input_number(message=tempo_message,
                           starting=0,
                           ending=300,
                           allow_no_input=False)
  # get note duration
  print(note_duration)
  note = get_input_number(message="Enter your note value here: ",
                          starting=0,
                          ending=8,
                          allow_no_input=False)

  note_duration_practiced = note_duration_dict.get(int(note))
  return tempo, note_duration_practiced



def extract_last_date(path, logfile):
  # logic -
  # read the last file name using log
  # get date from log and concatenate it to the actual file name
  # write a file name with new date as usual
  # half of
  with open(path + logfile) as f:
    try:
      dates = f.readlines()
      last_date = dates[-1]
    except IndexError or FileNotFoundError:
      last_date = ""
  return last_date


def concat_last_date_2file_name(filename, path, log_file):
  last_date = extract_last_date(path, log_file)[:-1]  #ignore new line
  filename_date = f"{filename}_{last_date}.xlsx"
  return filename_date


def df_to_dict(df):
  """

  :param dictionary:
  :return:
  """
  new = {}
  for key, value in df.iteritems():
    new[key] = list(value.values)
  return new


def series_to_dict(series):
  """

  :param series:
  :return:
  """
  new = {}
  for key, value in series.iteritems():
    new[key] = value
  return new


def merge_dicts_value(primary_dict, *dictionaries):
  """

  :param primary_dict:
  :param dictionaries:
  :return:
  """
  merged_dict = {}
  for dictionary in dictionaries:
    for key, value in primary_dict.items():
      if dictionary.get(key) is None:
        continue
      other_value = (int(dictionary[key])
                     if isinstance(dictionary[key], float)
                     else dictionary[key])

      if key not in merged_dict:
        merged_dict[key] = [value, other_value]
      else:
        merged_dict[key].append(other_value)
  return merged_dict

def todays_time_tempo_notation_df(time_dict, tempo_dict, notation_dict, index):
  """

  :param time_dict:
  :param tempo_dict:
  :param notation_dict:
  :return:
  """
  # get last row
  todays_tempo_values = tempo_dict.iloc[-1, :]
  todays_note_duration = notation_dict.iloc[-1, :]
  # convert to dictionary
  todays_notation_dict = series_to_dict(todays_note_duration)
  todays_tempo_dict = series_to_dict(todays_tempo_values)
  # merge all dictionaries
  todays_df = (pd.DataFrame()
              .append(pd.Series(
                                merge_dicts_value(time_dict,
                                                  todays_tempo_dict,
                                                  todays_notation_dict),
                                                  name=index),
                                ignore_index=False))

  todays_df["Interpretation"] = "Time, Tempo, Note_Value"

  return todays_df