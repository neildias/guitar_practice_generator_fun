from .core import *
from .timer import countdown
from .default_params import practice_lesson_header_message, total_lessons, lessons_key


flexible_message = (

  """Each session defaults to 30 mins in duration. Will this session with
  short/long, and by how much? Type 0.5 for by 50% short (reduced to half-time),
  type 0.2 for 20% or 2 for 200% of lesson time;
  
  -- for no change press Enter with no value: """

)

inflexible_message = (

  """Each session defaults to 30 mins in duration. Will this session with short?
  if yes, press 0.5 to cut the session by half;
  -- for no change press Enter with no value: """

)


def lesson_iterator(lessons_time: dict,
                    tempo_dict: dict,
                    note_duration_dict: dict,
                    lesson_practiced: str,
                    choice: str,
                    duration: str,
                    flexible: bool):
  """
  Iterates over the lesson dictionary, runs the timer according to each lesson
  and return a tuple of dictionaries of lesson, time and header values

  :param choice: str
  :param duration: str or float
  :param flexible: bool
  :return: tuple of dict: updated lessons_dict, dict_time, str of header values
  """

  topic_chosen = lessons_key[choice]
  relevant_lesson = total_lessons[topic_chosen]

  print(f'\nYou will be practicing the following under the {topic_chosen} '
        f'lesson: \n')

  # print for the user to know what s/he will be practicing
  print_keys(relevant_lesson, duration = duration, message="mins")

  # a string of practice heads to add in the notes sheet
  # only last practice header recorded in case multiple sessions chosen

  for lesson, time in relevant_lesson.items():

    if flexible:
      
      # allow user to skip lesson
      play_lesson = input(f"\nPress enter to start practicing {lesson}; "
                          f"and 'n' to skip it: ")
      
      if play_lesson == 'n':
          print(f"\nWARNING! You have chosen to skip {lesson}")
          continue

    elif not flexible:
      input(f"\nPress enter to start practicing {lesson}: ")

    # for lesson in topic_head:
    # if duration chosen, increase or decrease time by mul with duration
    if duration:
      time = time * float(duration)
      
    # add time to an already existing practiced lesson
    if lesson in lessons_time:
      lessons_time[lesson] += time
    else:
      lessons_time[lesson] = time  # introduce the lesson

    # run timer
    counter_ran = countdown(time, lesson)
    
    if counter_ran:
      # update lesson practiced
      lesson_practiced = f"{lesson} | "
      
      # ask the user for tempo used
      tempo, note_duration_ = get_tempo_note_duration()
      
      # update tempo_dict and note_duration_dict
      tempo_dict[lesson] = tempo
      note_duration_dict[lesson] = note_duration_
      
    else:
      # populate with 0 values if the counter does not run
      # to avoid keyerrors in later processes
      # all dictionaries must have the same keys
      tempo_dict[lesson] = 0
      note_duration_dict[lesson] = 0
      
    print()

  return lessons_time, tempo_dict, note_duration_dict, lesson_practiced


def scheduler(flexible=True):
  """
  Helps the user choose between lesson headers,
  
  :return: dict | updated lessons_dict
  """
  
  keep_practicing = True
  lessons_time = dict()
  practice_notes_dict = dict()
  tempo_dict = dict()
  note_duration_dict = dict()
  session = 0
  lesson_practiced = ""
  
  # message to customise timing depending on flexible param
  if flexible:
    customise_duration_message = flexible_message

  elif not flexible:
    customise_duration_message = inflexible_message

  while keep_practicing:
    
    session += 1
    
    practice_time = get_input_number(customise_duration_message,
                                     starting=0,
                                     ending=10,
                                     allow_no_input=True)
    
    print(practice_lesson_header_message)
    
    practice_message = ("\nWhich among the above categories do you "
                        "want to practice now? Select by number: ")
    
    practice_header = get_input_number(message=practice_message,
                                       starting=1,
                                       ending=6,
                                       allow_no_input=False)
    
    # validate header choice
    
    if practice_header > 0 and practice_header < 7:
      
      # make classical music the default practice routine
      practice_header = 1 if not practice_header else practice_header

      practice_data_dict, tempo_dict2, note_dura_dict, practiced_lessons = (
        
                lesson_iterator(
                        # pass empty or non-empty dicts
                        lessons_time=lessons_time,
                        tempo_dict=tempo_dict,
                        note_duration_dict=note_duration_dict,
                        lesson_practiced=lesson_practiced,
                        # other params
                        choice=practice_header,
                        duration=practice_time,
                        flexible=flexible,
                )
      )

      # update dicts with new practice data
      lessons_time.update(practice_data_dict)
      tempo_dict.update(tempo_dict2)
      note_duration_dict.update(note_dura_dict)
      
      # set lesson_practiced to the old one received above
      lesson_practiced = practiced_lessons

      # update headers.
      practice_notes_dict = update_dictionary(dictionary=practice_notes_dict,
                                              key="Topics Practiced",
                                              value=practiced_lessons,
                                              by_concat=True,
                                              handle_error=True)
      
      
      # ask for notes here.
      practice_message = input("\nWrite any notes or comments on this"
                                 " session here. Press Enter thereafter\n")
      
      # if its the first session enter the data
      formatted_msg = f"Session     {session} : {practice_message}    |    "
      
      practice_notes_dict = update_dictionary(dictionary=practice_notes_dict,
                                              key="Notes",
                                              value=formatted_msg,
                                              by_concat=True)
      
      
    # ensure valid options are selected
    else:
      print("\nWrong input! Choose between the number 1 and 6 next time. :)")

    if flexible:
      # check if the user wants to continue practice, if no,
      # break the loop
      another_practice = input("\n\nDo you wish to practice another header."
                                " Press y if yes, else enter: ")
      if not another_practice == "y":
        keep_practicing = False

    elif not flexible:
      # if not flexible, dont let user opt for another lesson
      keep_practicing = False

  return (lessons_time,
          tempo_dict,
          note_duration_dict,
          practice_notes_dict)
