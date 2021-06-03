import pandas as pd
from datetime import date
from pprint import pprint
import os


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
  # change directory
  change_directory = input(
    f"Do you want to change the current file path: {path}, "
    f"or the current file_name: '{filename}'.\n"
    f"Or add to the current topics/heads of practice: ? "
    f"Enter 'y' if you want to change that, else press ENTER. "
  )
  if change_directory == 'y':
    invalid_directory = True
    while invalid_directory:
      file_directory = input('Type a new path, else press ENTER for no change ')
      # if opted not to change
      if not file_directory:
        invalid_directory = False
      else: # if directory inputted test if its a valid file path
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
      else: # check if inputted filename is valid
        if file_name.isalnum():
          invalid_filename = False
        else:
          print("The file name is invalid. Enter again.")

    # alter topic headers
    invalid_topic_head = True
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


def read_create_database_object(path: str, filename: str, data_dict: dict):
  """
  Returns a dataframe based on existing files or by creating a new one

  :param path: str
  :param filename: str
  :param data_dict: dict
  :return: df
  """
  try:
    # check if an excel file is available
    df = pd.read_excel(path + filename, index_col=0)
    print("Found existing database")

  except FileNotFoundError as e:
    # if unavailable create a dataframe, to be later exported as exce;
    # print(e)
    print("Existing database not found. Creating a new database (dataframe)\n")

    df = pd.DataFrame(data_dict,
                      index=pd.date_range(start="06-03-2021", periods=1, freq="D"))

  return df


# get date for the index column of the dateframe for the new inputs
def get_date():
  """
  Retrieve custom or current date in the appropriate format

  :return: python or pandas date object. Later if user inputs a date
  """

  while True:
    custom_date = input(
      "If the entry is for a custom date, enter after typing date in dd-mm-yyyy;"
      " else press ENTER : "
    )
    if not custom_date:
      return date.today()
    else:
      try:
        return pd.to_datetime(custom_date, format="%d-%m-%Y")
      except:
        print("Wrong Input!!! Either press plain enter key, or provide date in "
              "dd-mm-yyyy format. Try again!")


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
      if value < 60 * 8:                       # less than 8 hours of practice
        bad_input = False
        print()
      else:
        print("Bad input received. Input a (whole) number less than 480... "
              "Try again!!!")

    except ValueError as e:
      # print(e)
      print("Minutes entered must be a whole number. Try again!!!")
  return value


def get_data_points(data_dict: dict):
  """
  Returns a dictionary of updated values for each header

  :param data_dict: dict | dictionary of topics and values
  :return: dict | updates in dictionary dtype
  """

  updates_to_add = dict()
  towards_total_minutes = 0

  for key in data_dict.keys():
    value = get_minutes(key)
    updates_to_add[key] = value
    towards_total_minutes += value

  updates_to_add["Total Mins"] = towards_total_minutes

  return updates_to_add