import pandas as pd
from datetime import date
import os
from pprint import pprint
from utils.default_params import record_log
from utils.core import concat_last_date_2file_name


def get_file_path(path: str, filename: str, data_dict: dict):
  """
  Lets user change file path, filename and add more topic headers to the
  practice routine

  :param path: str
  :param filename: str
  :param data_dict: dict
  :return: None if no change opted else returns filepath, filename,
           modified_data_dict
  """
  
  # instantiate new variables
  file_directory = file_name = ""

  # change directory
  change_directory = input(
    f"Do you want to change the current file path: {path}, "
    f"or the current file_name: '{filename}'.\n"
    f"Or add to the current topics/heads of practice: ? "
    f"Enter 'y' if you want to change that, else press ENTER : "
  )
  
  if change_directory == 'y':
    
    invalid_directory = True
    
    while invalid_directory:
      
      file_directory = input('Type a new path, else press ENTER for no change ')
      
      # if opted not to change
      if not file_directory:
        invalid_directory = False
      
      else:  # if directory inputted test if its a valid file path
        
        if os.path.exists(file_directory):
          invalid_directory = False
        
        else:
          print("Invalid file directory. Enter a valid file directory")

    # change filename
    invalid_filename = True
    
    while invalid_filename:
      
      file_name = input("Type new filename, else press ENTER for no change ")
      
      # if opted not to change
      if not file_name:
        invalid_filename = False
      
      else:  # check if inputted filename is valid
        
        if file_name.isalnum():
          invalid_filename = False
        
        else:
          print("The file name is invalid. Enter again.")

    # alter topic headers
    
    print("The current heads of practice are as follows: ")
    
    pprint([key for key in data_dict.keys()])
    
    change_topic_headers = input(
      "Press y to opt to change the topic headers, else type ENTER "
    )
    
    if change_topic_headers == "y":
      new_topic_headers = input(
        "Type the name of new topic heads separated by space, then enter : "
      )
      
      for topic_head in new_topic_headers.split():
        # topic head sanity check
        
        while not topic_head.isalpha():
          topic_head = input(
            f"Previous entry {topic_head} must be all alphabets. Try again: "
          )
        
        data_dict[topic_head] = 0
    
    return file_directory, file_name, data_dict

  else:   # No change
    return None, None, None


def create_database_object(data_dict: dict, prnt_msg=True):
  """
  Create a new dataframe. The function is to be used if reading an existing
  excel file has failed.

  :param data_dict: dict
  :param prnt_msg: bool
  :return: tuple | 3 dataframes
  """
  
  if prnt_msg:
    print("Existing database not found. Creating a new database (dataframe)\n")

  # needed to create the dataframe
  today_d = date.today()

  today_pandas_index = pd.date_range(start=str(today_d), periods=1, freq="D")

  # time_log sheet
  # since index is needed to create a scalar df, it will used for creation of
  # df and dropped after the fact
  df_time_log = pd.DataFrame(data_dict, index=today_pandas_index)
  df_time_log["Total Mins"] = 0  # last col
  df_time_log.drop(today_pandas_index, inplace=True)

  # tempo sheet
  df_tempo = pd.DataFrame(data_dict, index=today_pandas_index)
  df_tempo.drop(today_pandas_index, inplace=True)
  
  # notation sheet
  df_notation = pd.DataFrame(data_dict, index=today_pandas_index)
  df_notation.drop(today_pandas_index, inplace=True)
  
  # notes sheet
  df_notes = pd.DataFrame({"Notes": ""}, index=today_pandas_index)
  df_notes.drop(today_pandas_index, inplace=True)

  # todays sheet
  df_today = pd.DataFrame(index=today_pandas_index, columns="lesson_1 "
                                                            "lesson2".split())

  return df_time_log, df_tempo, df_notation, df_notes, df_today


def read_database_object(path: str,
                         filename: str,
                         data_dict: dict,
                         has_date_ending=True,
                         ):
  """
  Loads the main file, and returns a dataframe based on existing files or by
  creating a new one

  :param path: str
  :param filename: str
  :param data_dict: dict
  :return: df
  """
  # check if default directory exists,
  # if not os.path.exists():
  #   return print("ERROR! Default Directory not found. Rerun program and use "
  #                "custom settings.")
  
  try:
    
    if ".xlsx" in filename and has_date_ending:
      
      # strip file extension
      filename = filename[:-5]
      complete_path = path + concat_last_date_2file_name(filename,
                                                         path,
                                                         record_log)
    else:
      complete_path = path + filename
    # check if an excel file is available
    
    df_dict = pd.read_excel(complete_path,
                            sheet_name = "Time_Log Tempo Notation "
                                         "Notes Today".split(),
                            index_col = 0)
    
    # get dataframe from the above dictionary object
    df_time_log = df_dict["Time_Log"]
    df_tempo = df_dict["Tempo"]
    df_notation = df_dict["Notation"]
    df_notes = df_dict["Notes"]
    df_today = df_dict["Today"]

    print(f"\nFound existing database at {path+complete_path} \n")

  except FileNotFoundError:
    
    # if unavailable create a dataframe, to be later exported as excel;
    all_dfs = create_database_object(data_dict)
    
    df_time_log, df_tempo, df_notation, df_notes, df_today = all_dfs

  except Exception as e:
    
    print(f"\nERROR! Encountered {e}")
    
    all_dfs = create_database_object(data_dict)

    df_time_log, df_tempo, df_notation, df_notes, df_today = all_dfs

  return df_time_log, df_tempo, df_notation, df_notes, df_today
