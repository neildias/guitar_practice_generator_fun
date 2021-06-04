from datetime import date, time, datetime
from time import sleep
#from countdown_timer import get_hours_minutes_seconds
try:
  import countdown_timer
except:
  from . import countdown_timer
import utils
from tkinter import *
# try:
#   from utils.utils import to_speech
# except ImportError:
#   from .utils import to_speech




def hr_min_sec_to_secs(hour: int, mins: int, second: int):
  """
  Converts hours, mins and seconds and returns consolidated seconds.
  Used with datetime.now() object, and its hour, minutes and seconds attributes

  :param hour: int
  :param mins: int
  :param second: int
  :return: int
  """

  hour_to_seconds = hour*60*60
  mins_to_seconds = mins*60
  return hour_to_seconds+mins_to_seconds+second


def string_to_time(time: str):
  """

  :param time:
  :return:
  """
  return datetime.strptime(time, "%H:%M:%S")



def combine_datetime_time(today: "datatime.date", hr: int, min: int, sec: int):
  """
  Combines datetime.date and int values of hrs, min and seconds to a datetime
  object

  :param today: "datatime.date"
  :param hr: int
  :param min: int
  :param sec: int
  :return: datetime object
  """

  time_object = time(hr, min, sec)
  combine = datetime.combine(today, time_object)
  return combine


def get_start_stop_time(time_in_seconds: int):
  """
  returns Start and Stop time. Start time being the current time and stop time
  being the time retrieved from adding the input to the current time

  :param time_in_seconds:
  :return: datetime objects | start_time, stop_time
  """

  today = date.today()
  now = datetime.now()

  # split hour, minute, second from now
  start_hour, start_minute, start_second = now.hour, now.minute, now.second

  # convert the above split into seconds
  current_time_seconds = hr_min_sec_to_secs(start_hour,
                                            start_minute,
                                            start_second)

  # get total time in seconds for stop time
  stop_time_seconds = current_time_seconds + time_in_seconds

  # convert the above into hours, minutes, seconds
  stop_hour, stop_minute, stop_second = countdown_timer.get_hours_minutes_seconds(
    stop_time_seconds
  )

  # convert and return start and stop time as datetime objects
  current_time = combine_datetime_time(today, start_hour, start_minute,
                                   start_second)
  stop_time = combine_datetime_time(today, stop_hour, stop_minute, stop_second)
  return current_time, stop_time


# def GUI_Countdown(start=300):
#
#   while start>0:
#     print(start)
#     start_time, stop_time = get_start_stop_time(start)
#     sleep(1)
#     start -= 1
#     time_remaining = stop_time - start_time
#     lb = Label(root,
#                font=('calibri', 50, 'bold'), background="black",
#                foreground="white")
#     lb.pack(anchor="center")
#     #lb.config(text=time_remaining)
#     #lb.after(200, GUI_Countdown)

def gui_counter(initial_seconds: int, label_object=None):
  """

  :param initial_seconds:
  :param label_object: tkinter label object
  :return:
  """
  # freeze stop time
  _, stop_time = get_start_stop_time(initial_seconds)

  # if the user does not supply the tkinter object
  if not label_object:
    root = Tk()
    root.title(f"Practice Countdown for Mastery")
    label_object = Label(root,
                         font=('calibri', 50, 'bold'),
                         background="black",
                         foreground="white")
    label_object.pack(anchor="ne")

  def countdown(seconds_remaining=initial_seconds):

    # stop when the counter turns to zero
    if seconds_remaining == 1:
      return

    # new current time to keep track of lapsed time
    now, _ = get_start_stop_time(seconds_remaining)
    # update seconds remaining
    seconds_remaining -= 1
    # calculate remaining time
    timer = stop_time - now
    # display GUI
    label_object.config(text=timer)
    # call the same function recursively
    label_object.after(1000, countdown, seconds_remaining)
    if seconds_remaining > 0:
      mainloop()

  return countdown


def gui_timer(user_topic_timings: dict, label_object=None):
  """
  Runs the countdown timer over the users input dict
  :param user_topic_timings: dict
  :return: None
  """
  for key in user_topic_timings.keys():
    seconds = user_topic_timings[key] * 60
    print("=" * 35)
    message_before_practice = (f"\nYou will be practicing '{key.upper()}' now. "
                               f"Whenever you are ready, press enter to begin you"
                               f" practice. \nThis will automatically get "
                               f"registered on your practice tracker.")

    # inform the user about the start of the session
    print(message_before_practice)  # through console
    utils.utils.to_speech(message_before_practice)  # through speech
    input()
    input("Are you sure you are ready? Press Enter if so")
    gui_counter(seconds)()
    # warn user
    utils.utils.to_speech("You may begin your practice now. ")
    # get the gui clock
    gui_counter(seconds, label_object)

    sleep(seconds)
    utils.utils.to_speech("You may stop your practice.")

  print("\nCongratulations! You have successfully finished your practice "
        "session. ")
  print("\nYou have move one session closer to your goals. Good day!")


# lb = Label(root,
#            font=('calibri', 50, 'bold'), background="black", foreground="white")
# lb.pack(anchor="ne")
# #gui_counter_test = gui_counter(300)
# #gui_counter_test(295)
# mainloop()
