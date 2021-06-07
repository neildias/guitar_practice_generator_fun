# A useful script when the practice session is needed real time and
# uses preset lessons

import pandas as pd
from datetime import date
import time


path = "P:\\"

filename = "guitar_practice_tracker.xlsx"

today = date.today()

topics = {
    "Music_Theory": 0,
    "Sight Reading (Other non Graded Pieces)": 0,
    "Ear Training": 0,
    "Sight Playing (Graded Studies|Classical Pieces)": 0,
    "Kitharologus": 0,
    "Rhythm (Song) Practice": 0,
    "Lead (Song) Pieces": 0,
    "FretBoard Mastery": 0,
    "Work on Scales": 0,
    "Strum Chords": 0,
    "Arpeggiate Chords": 0,
    "Slurs": 0,
    "Vibrato": 0,
    "Slide": 0,
    "Bends": 0,
    "Picado": 0,
    "Rasgeo": 0,
    "Pulgar": 0,
    "Alzapua": 0,
    "Golpe": 0,
    "Natural Harmonics": 0,
    "Artificial Harmonics": 0,
    # "Solea": 0,
    # "Alegrias": 0,
    # "Tangos": 0,
    # "Seguiriya": 0,
    # "Tarantas": 0,
    # "Granainas": 0,
    # "Bulerias": 0,
    "Improvisation": 0,
    # "Guitar Licks": 0,
    # "Flamenco RH": 0,
    # "Flamenco LH": 0,
    "Tremelo": 0,
    # "Sweep Picking": 0,
    # "Hybrid Picking": 0,
    # "Tapping": 0,
    # "Harp Harmonics": 0,
    # "Slap Harmonics:": 0,
    # "Percussive": 0,
    # "Whammy bar": 0,
    # "Pedals": 0,
  }

lesson_1 = {

    # Classical
    # lesson 1 total 30 mins
    "Spider Warmup": 2, #5,
    "Ear Training": 2,  #5,
    "Sight Playing (Graded Studies|Classical Pieces)": 2, #20,

}

lesson_2 = {

    # Scales
    "Scales Pick": 1, #10,
    "slurs": 1, #5,
    "Vibrato": 1, #5,
    "Picado": 1, #10,
}

lesson_3 = {

    # technical workout
    # lesson 2 total 35 mins
    "FretBoard Mastery": 1, #5,
    "Kitharologus": 1, #20,
    "Natural Harmonics": 1, #5,
}

# add chord workout on even days of the week
add_chord_workout = "Strum Chords" if today.day % 2 == 0 else "Arpeggiate Chords"

lesson_4 = {

    # Chords
    "Strum Chords": 1, #10,
    # strum on even days, else Arpeggiate
    add_chord_workout: 1, #10,
    "Rasgeo": 1, #10,

}

# choose Improvisation on even days of the week
creative_workout = "Improvisation" if today.day % 2 == 0 else "Song (Rhythm)"

lesson_5 = {

    # technical workout - others
    # Improvise on even days, else play rhythm songs
    creative_workout: 1, #10,
    "Bends": 1, #5,
    "Alzapua": 1, #5,
    "Tremelo": 1, #5,
    "Chord Ear Training": 1, #5,

}

lesson_6 = {
    "Music_Theory": 30,
}

# consolidating the above lessons
total_lessons = {

    "Classical Studies" : lesson_1,
    "Scales": lesson_2,
    "Kitharologus": lesson_3,
    "Chords": lesson_4,
    "Creative": lesson_5,
    "Music Theory": lesson_6,

}

lessons_key = {

    "1": "Classical Studies",
    "2":"Scales" ,
    "3":"Kitharologus",
    "4":"Chords",
    "5":"Creative",
    "6": "Music Theory",

}


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


def get_hours_minutes_seconds(time_in_seconds: int):
  """
  Converts seconds to hours, minute and seconds

  :param time_in_seconds: int
  :return: int | hours, minutes, seconds
  """

  minutes, seconds = divmod(time_in_seconds, 60)
  hours, minutes = divmod(minutes, 60)
  return hours, minutes, seconds


def countdown(time_in_minutes: int, topic_header: str):
  """
  :param time_in_seconds: int
  :return: None
  """
  seconds = 60
  timer = abs(int(float(time_in_minutes*seconds)))

  print(f"\nCountdown Timer for '{topic_header}': Practice non-stop till "
        f"zero")
  print("-------------------------------------------------------------")

  # print timer
  while timer > 0:
    hours, minutes, seconds = get_hours_minutes_seconds(timer)
    time_to_display = f"\r{str(hours).zfill(2)}:{str(minutes).zfill(2)}" \
                      f":{str(seconds).zfill(2)}"
    print(time_to_display, end="")
    # print(time_to_display + "\r", end="")
    time.sleep(1)
    timer -= 1

  if timer == 0:
    return


def lesson_iterator(choice: str, short: bool=False):
  """
  Iterates over the lesson dictionary

  :param choice: str
  :param short: bool
  :return: dict: updated lessons_dict
  """
  lessons_time = {}
  topic_chosen = lessons_key[choice]
  relevant_lesson = total_lessons[topic_chosen]
  print(f'You will be practicing this {relevant_lesson.keys()}.')
  for lesson, time in relevant_lesson.items():
    input("Press enter to start the lesson... ")
    #for lesson in topic_head:
    if short:
      time = time // 2
    lessons_time[lesson] = time
    countdown(time, lesson)
    print("\n")

  return lessons_time


def scheduler():
  """
  Helps the user choose between lesson headers,
  :return: dict | updated lessons_dict
  """
  keep_practicing = True
  lessons_time = dict()
  while keep_practicing:
    practice_time = input("Will this session with short? Press 1 for yes, else Enter: ")
    practice_time = True if practice_time == "1" else False
    print("""\n

         PRACTICE LESSON HEADERS
         =======================\n

            1. Classical Studies
            2. Scales
            3. Kitharologus
            4. Chords
            5. Creative
            6. Music Theory

        """)

    practice_header = input("\nWhich among the above categories do you want to "
                                "practice now? Select by number: ")
    practice_header = "1" if not practice_header else practice_header

    practice_data_dict = lesson_iterator(choice=practice_header,
                                           short=practice_time)

    lessons_time.update(practice_data_dict)

    another_practice = input("Do you wish to practice another header. \
                              Press y if yes, else enter: ")
    if not another_practice == "y":
      keep_practicing = False
  return lessons_time


def get_data_points(data_dict: dict):
  """
  Returns a dictionary of updated values for each header

  :param data_dict: dict | dictionary of topics and values
  :return: dict | updates in dictionary data type
  """

  updates_to_add = dict()
  towards_total_minutes = 0
  for lesson, time in data_dict.items():
    updates_to_add[lesson] = time
    towards_total_minutes += time
  updates_to_add["Total Mins"] = towards_total_minutes
  updates_to_add["Lowest Tempo"] = int(input(
                                    "\nPlease input lowest temp practiced at: ")
  )
  updates_to_add["Highest Tempo"] = int(input(
                                   "\nPlease input highest temp practiced at: ")
  )
  return updates_to_add


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


if __name__ == '__main__':
    # get new_path, filename if the user chooses
    new_path, new_filename, new_topic_dict = get_file_path(path,
                                                           filename,
                                                           topics)

    path = new_path if new_path else path
    filename = new_filename+".xlsx" if new_filename else filename
    topics = new_topic_dict if new_topic_dict else topics

    # get data
    df = read_create_database_object(path, filename, topics)

    # store date in the update_date variable
    update_date = get_date()
    print()

    # get a dictionary of key, value updates
    topics_practiced = scheduler()
    updates = get_data_points(topics_practiced)

    # update the dataframe
    df = df.append(pd.Series(updates,
                             name=update_date),
                   ignore_index=False)

    # ensure Total Mins is Last col
    position = len(df.columns) - 1
    df = column_reorder(df, "Total Mins", position)

    print(df.T)

    # export df as excel doc with the same file name
    df.fillna(0).to_excel(path + filename, index=True)