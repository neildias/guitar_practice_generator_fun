from utils.default_params import today, note_duration, note_duration_dict
import pandas as pd
import numpy as np


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
  for key, val in dictionary.items():
    
    if value:
      
      if not duration:
        print(key, value, message)
        
      elif isinstance(duration, float):
        print(key, round(value*duration,2), message)
    
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
                          ending=9,
                          allow_no_input=False)

  note_duration_practiced = note_duration_dict.get(int(note))
  
  return tempo, note_duration_practiced



def extract_last_date(path, logfile):
  """
  
  :param path:
  :param logfile:
  :return:
  """

  with open(path + logfile) as f:
    
    try:
      dates = f.readlines()
      last_date = dates[-1]
      
    except IndexError or FileNotFoundError:
      last_date = ""
      
  return last_date


def concat_last_date_2file_name(filename, path, log_file):
  """
  
  :param filename:
  :param path:
  :param log_file:
  :return:
  """
  
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


def todays_df(time_dict, tempo_dict, notation_dict, index):
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

  final = {}
  counter = 1
  
  for key in time_dict.keys():
    
    if key == "Total Mins":
      continue
      
    final["lesson_" + str(counter)] = [key,
                                       time_dict[key],
                                       todays_notation_dict[key],
                                       todays_tempo_dict[key]]
    counter+=1


  # create multiindex
  time_keys = np.array([index, index, index, index] )
  tempo_keys = np.array(["LessonName", "Time", "tempo", "note"])
  multiindex = [time_keys, tempo_keys]

  todays_multi_index_df = pd.DataFrame(data=final, index=multiindex)

  return todays_multi_index_df


def todays_series(time_dict, tempo_dict, notation_dict, index):
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

  final = {}
  counter = 1
  
  for key in time_dict.keys():
    
    if key == "Total Mins":
      continue
      
    final["lesson_" + str(counter)] = [key,
                                       time_dict[key],
                                       todays_notation_dict[key],
                                       todays_tempo_dict[key]]
    counter+=1

  # create multiindex
  time_keys = np.array([str(index)] * 4)
  tempo_keys = np.array(["LessonName", "Time", "tempo", "note"])
  multiindex = [time_keys, tempo_keys]

  todays_multi_index_series = pd.Series(data=final,
                                        index=multiindex,
                                        name=index)

  return todays_multi_index_series


def update_dictionary(dictionary: dict,
                      key: str,
                      value: str,
                      by_concat: bool = True,
                      handle_error: bool = True,
                      keep_duplicates: bool = False):
  """
  Updates dictionary.
  
  if key absent updates the values
  
  If key already present, attempts to concat values, but if it fails it
  replaces the old value.
  
  keep_duplicates only used if by_concat is set to True
  
  :param dictionary: dict
  :param key: str
  :param value: str
  :param by: bool
  :param handle_error: bool
  :param keep_duplicates: bool
  :return:
  """
  assert isinstance(dictionary, dict), f"Dict data type expected, got " \
                                       f"{type(dictionary)}"
  try:
    
    if by_concat:
      
      # check if not first entry
      if key in dictionary.keys():
 
        if not keep_duplicates:
          # avoid duplication of values
          if value in dictionary[key]:
            pass
          
          else:
            print("first else")
            dictionary[key] += value
        
        else:
          print("second else")
          # ignore duplication if any
          dictionary[key] += value
      
      # if first entry
      if key not in dictionary.keys():
        dictionary[key] = value
  
  except:
    
    print("Concatenation of dictionary failed. Replacing old value")
    
    # replace original value
    if handle_error:
      dictionary[key] = value
  
  if not by_concat:
    # replace
    dictionary[key] = value
  
  return dictionary
  