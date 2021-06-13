from numpy import random
import utils
import time

musical_notes = "Ah B C D E F G".split()  # Ah not A; help gTTS pronounce
print(musical_notes, "\n", "="*35, "\n")    # aesthetics


def multiple_strings_names_to_text(counter: int):
  """
  A helper function for below functions

  :param counter: int
  :return: str | strings names in string format
  """

  total_strings = "One Two Three Four Five Six".split()

  string_names = []
  for _ in range(counter):
    string_chosen = total_strings[random.randint(len(total_strings))]
    # remove the string name for the next iteration
    total_strings.remove(string_chosen)
    string_names.append(string_chosen)

  string_names_to_text = " ".join(string_names)

  return string_names_to_text


def random_notes(iterations: int = 100, time_gap: float = 1.):
  """
  Prints random musical notes in space of the time_gap mentioned for the
  iteration asked.

  :param iterations: int
  :param time_gap: float
  :return: None
  """

  for _ in range(iterations):
    note = random.choice(musical_notes)
    print(note)
    connection_passed = utils.to_speech(voice_this=note)
    if not connection_passed:
      return print("ERROR: Session Terminated Abruptly")
    time.sleep(time_gap)


def find_tonic_on(random_tonic: bool = False,
                  iterations: int = 10,
                  how_many_strings: int = 2,
                  time_gap: float = 5.,
                  how_many_notes: int = 1):
  """
  Use case with random_tonic == FAlSE:
  Spells out random name(s) of the string on which a note of users choice is to
  be played

  Use case with random_tonic == TRUE:
  Spells out random name(s) of the strings along with random names of note(s).
  The random notes are to be played on notes suggested

  Note: how_many_notes argument is only used if random_tonic is used.

  :param random_tonic: bool
  :param iterations: int | how many times to spell out random notes/strings
  :param how_many_strings: int | how many random string names to spell out
  :param time_gap: float | time in seconds
  :param how_many_notes: float | random notes to be generated
  :return: None
  """

  for _ in range(iterations):

    if random_tonic:
      # choose and print random notes
      random_notes(how_many_notes, 3)

    # choose random strings
    strings_to_speech = multiple_strings_names_to_text(how_many_strings)
    connection_passed = utils.to_speech(voice_this=strings_to_speech)
    if not connection_passed:
      return print("ERROR: Session Terminated Abruptly")
    time.sleep(time_gap*how_many_strings)
    print("="*10)


if __name__ == "__main__":

  random_notes(iterations=90, time_gap=5.25)

  # uncomment below line to stop here
  # sys.exit()

  find_tonic_on(random_tonic=False,           # True to get random notes
                iterations=30,
                how_many_strings=2,           # value 1 through 6
                time_gap=5.,
                how_many_notes=1)             # recommended below 4
