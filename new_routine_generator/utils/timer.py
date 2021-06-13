import time
from gtts import gTTS

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
  if timer == 0:
    return print("Custom duration chosen is too short. This lesson is being skipped.")

  countdown_timer_message = (
  f"\nCountdown Timer for '{topic_header}': Practice non-stop till zero"
  )
  # print timer message plus underline
  print(countdown_timer_message)
  print("-"*len(countdown_timer_message))

  # print timer until timer == 0
  while timer > -1:
    hours, minutes, seconds = get_hours_minutes_seconds(timer)
    time_to_display = f"\r{str(hours).zfill(2)}:{str(minutes).zfill(2)}" \
                      f":{str(seconds).zfill(2)}"
    print(time_to_display, end="")
    # print(time_to_display + "\r", end="")
    time.sleep(1)
    timer -= 1


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
