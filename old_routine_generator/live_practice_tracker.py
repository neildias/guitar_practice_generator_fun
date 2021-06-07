# A useful script when the practice session is needed real time and
# uses preset lessons

import pandas as pd
from datetime import date
import time
from utils import practice_headers, utilities, countdown_timer


# hardcoded path
path = practice_headers.path
filename = practice_headers.filename
topics = practice_headers.topics

today = date.today()

lesson_1 = {

    # Classical
    # lesson 1 total 30 mins
    "Spider Warmup": 5,
    "Ear Training": 5,
    "Sight Playing (Graded Studies|Classical Pieces)": 20,

}

lesson_2 = {

    # Scales
    "Scales Pick": 10,
    "slurs": 5,
    "Vibrato": 5,
    "Picado": 10,
}

lesson_3 = {

    # technical workout
    # lesson 2 total 35 mins
    "FretBoard Mastery": 5,
    "Kitharologus": 20,
    "Natural Harmonics": 5,
}

# add chord workout on even days of the week
add_chord_workout = "Strum Chords" if today.day % 2 == 0 else "Arpeggiate Chords"

lesson_4 = {

    # Chords
    "Strum Chords": 10,
    # strum on even days, else Arpeggiate
    add_chord_workout: 10,
    "Rasgeo": 10,

}

# choose Improvisation on even days of the week
creative_workout = "Improvisation" if today.day % 2 == 0 else "Song (Rhythm)"

lesson_5 = {

    # technical workout - others
    # Improvise on even days, else play rhythm songs
    creative_workout: 10,
    "Bends": 5,
    "Alzapua": 5,
    "Tremelo": 5,
    "Chord Ear Training": 5,

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
    hours, minutes, seconds = countdown_timer.get_hours_minutes_seconds(timer)
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
    new_path, new_filename, new_topic_dict = utilities.get_file_path(path,
                                                                     filename,
                                                                     topics)

    path = new_path if new_path else path
    filename = new_filename+".xlsx" if new_filename else filename
    topics = new_topic_dict if new_topic_dict else topics

    # get data
    df = utilities.read_create_database_object(path, filename, topics)

    # store date in the update_date variable
    update_date = utilities.get_date()
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
    df = utilities.column_reorder(df, "Total Mins", position)

    print(df.T)

    # export df as excel doc with the same file name
    df.fillna(0).to_excel(path + filename, index=True)
