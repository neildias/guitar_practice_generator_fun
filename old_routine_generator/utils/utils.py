import pandas as pd
from datetime import date
from pprint import pprint
import os
from gtts import gTTS


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
    f"Enter 'y' if you want to change that, else press ENTER. "
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

  except FileNotFoundError:
    # if unavailable create a dataframe, to be later exported as excel;
    print("Existing database not found. Creating a new database (dataframe)\n")

    df = pd.DataFrame(data_dict,
                      index=pd.date_range(start="06-03-2021",
                                          periods=1,
                                          freq="D"))
    df["Total Mins"] = 0  # last col

  return df


def column_reorder(df, col_name, position):
  """
  Reorders df columns
  :param df:
  :param col_name:
  :param position:
  :return:
  """
  temp_series = df[col_name]
  df = df.drop(col_name, axis=1)
  df.insert(loc=position, column=col_name, value=temp_series)
  return df


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
      return date.today()
    else:
      try:
        return pd.to_datetime(custom_date, format="%d-%m-%Y")
      except ValueError:
        print("Wrong Input!!! Either press plain enter key, or provide date in "
              "dd-mm-yyyy format. Try again!")


# get values to be inputted in the dataframe
def get_minutes(key: str):
  """
  get, authenticate and return input value in minutes

  :param : str | key in a dict
  :return: int | minutes
  """
  value = ""
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

    except ValueError:
      print("Minutes entered must be a whole number. Try again!!!")
  return value


def get_data_points(data_dict: dict):
  """
  Returns a dictionary of updated values for each header

  :param data_dict: dict | dictionary of topics and values
  :return: dict | updates in dictionary data type
  """

  updates_to_add = dict()
  towards_total_minutes = 0

  for key in data_dict.keys():
    value = get_minutes(key)
    updates_to_add[key] = value
    towards_total_minutes += value

  updates_to_add["Total Mins"] = towards_total_minutes

  return updates_to_add


def topic_duration_capture(data_dict: dict):
  """
  Gets the choice of practice from user along with minutes the user wants to
  practice

  :param data_dict:
  :return: dict | modified data_dict
  """

  topic_duration_keeper = dict()
  for key in data_dict.keys():
    choice = input(f"\n'{key.upper()}' -- wanna practice right now? "
                   f"Press 'y' + Enter for yes, else Enter: ")
    if choice:
      while True:
        try:
          topic_duration_keeper[key] = int(input("Enter time in minutes for "
                                                 f"practicing {key}). "))
          break
        except:
          print("Please enter time in minutes i.e. a number.")
  return topic_duration_keeper


def to_speech(voice_this: str):
  """
  A helper function for below functions

  :param voice_this: str
  :return: bool | True if not encountered any problem, else returns False
  """
  try:
    text_to_speech = gTTS(text=voice_this, lang='en', slow=False)
    text_to_speech.save("speech.mp3")
    # os.system("note.mp3")
    os.startfile(os.getcwd() + "\\speech.mp3")
    return True
  except:
    print("\nERROR: Unable to connect. Check your internet connection.")
    return False


def total_dict_values(dict_data: dict):
  """
  Returns the total values of all keys
  :param dict_data:
  :return: int
  """

  total = 0
  for key in dict_data.keys():
    total += dict_data[key]
  return total
