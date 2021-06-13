import utils
from flexible_tracker import live_practice_tracker


path = utils.path
filename = utils.current_filename
topics = utils.topics


def fixed_tracker(path: str,
                  filename: str,
                  topics: dict,
                  flexible=False):
  """

  :param path: str
  :param filename: str
  :param topics: dict
  :param flexible: bool
  :return:
  """
  live_practice_tracker(path=path,
                        filename=filename,
                        topics=topics,
                        flexible=flexible)


if __name__ == '__main__':
  live_practice_tracker(path, filename, topics, flexible=False)
