import time
from .utils import to_speech


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
  A simple countdown time keeper

  :param time_in_minutes:
  :param topic_header: str
  :return: None
  """
  seconds_ = 60
  run = True
  while run:

    try:
      timer = abs(int(float(time_in_minutes*seconds_)))

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
        run = False

    except KeyboardInterrupt:
      print("Exited the countdown timer.")
      break

    except:  # general exception
      print("Please enter a number")
      time_in_minutes = input("Enter Time in Minutes : ")


def countdown_clock(user_topic_timings: dict):
  """
  Runs the countdown timer over the users input dict
  :param user_topic_timings: dict
  :return: None
  """
  for key in user_topic_timings.keys():
    minutes = user_topic_timings[key]
    print("=" * 35)
    message_before_practice = (f"\nYou will be practicing '{key.upper()}' now. "
                               f"Whenever you are ready, press enter to begin you"
                               f" practice. \nThis will automatically get "
                               f"registered on your practice tracker.")

    # inform the user about the start of the session
    print(message_before_practice)  # through console
    to_speech(message_before_practice)  # through speech
    input()
    input("Are you sure you are ready? Press Enter if so")

    # warn user
    to_speech("You may begin your practice now. ")
    countdown(minutes, key)
    to_speech("You may stop your practice.")
    time.sleep(2)

  print("\nCongratulations! You have successfully finished your practice "
        "session. ")
  print("\nYou have move one session closer to your goals. Good day!")
