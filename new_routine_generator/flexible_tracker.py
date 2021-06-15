import os
import utils
import pandas as pd
import warnings


warnings.filterwarnings("ignore")

path, backup_path, cloud_path = utils.path, utils.backup_path, utils.cloud_path
filename = utils.main_file_name
topics = utils.topics


def live_practice_tracker(path: str,
                          filename: str,
                          topics: dict,
                          flexible: bool = True):
  """
  Combines all functions in the script to run the live practice tracking program
  
  :param path: str
  :param filename: str
  :param topics: dict
  :param flexible: bool
  :return:
  """
  
  custom_setting = input("Press enter to use default settings of the script,"
                         " else press any key : ")
  
  # if custom setting not chosen yet default dir does not exist exit the program
  if not custom_setting and not os.path.exists(path):
    return print("\nERROR! Default Directory not found. Rerun program and use "
                 "custom settings.")
  
  if custom_setting:
    # get new_path, filename if the user chooses
    new_path, new_filename, new_topic_dict = utils.get_file_path(path,
                                                                 filename,
                                                                 topics)
    
    path = new_path if new_path else path
    filename = new_filename + ".xlsx" if new_filename else filename
    topics = new_topic_dict if new_topic_dict else topics
  
  # get data
  all_dfs = utils.read_database_object(path, filename, topics)
  df_time_log, df_tempo, df_notation, df_notes, _ = all_dfs
  
  # store date in the update_date variable
  update_date = utils.today if not custom_setting else utils.get_date()
  print()
  
  # get a dictionary of key, value updates
  values = utils.scheduler(flexible=flexible)
  topics_practiced, tempo_dict, notation, practice_notes_dict = values
  # add total mins to topics_practiced
  complete_updates = utils.get_data_points(topics_practiced)
  # only todays values
  todays_update = utils.get_data_points(topics_practiced,
                                        only_practiced_items=True)
  
  # create respective dataframes
  df_time_log = (df_time_log
                 .append(pd.Series(complete_updates, name=update_date),
                         ignore_index=False)
                 .astype("float64"))
  
  # ensure Total Mins is Last col
  df_time_log = utils.column_reorder(df_time_log, "Total Mins").fillna(0)
  
  df_tempo = (df_tempo
              .append(pd.Series(tempo_dict, name=update_date),
                      ignore_index=False)
              .fillna(0))
  
  df_notation = (df_notation
                 .append(pd.Series(notation, name=update_date),
                         ignore_index=False)
                 .fillna(0))
  
  df_notes = df_notes.append(pd.Series(practice_notes_dict,
                                       name=update_date),
                             ignore_index=False)
  
  # ensure Notes is the last column
  df_notes = utils.column_reorder(df_notes, "Notes")
  
  df_today_log = utils.todays_df(todays_update,
                                 df_tempo,
                                 df_notation,
                                 update_date)
  
  # export df as excel doc with the same file name
  # date in name param is true by default
  files_to_write = df_time_log, df_tempo, df_notation, df_notes, df_today_log
  utils.data_to_excel(path, filename, *files_to_write)
  utils.data_to_excel(backup_path, filename, *files_to_write)
  utils.data_to_excel(cloud_path, filename, *files_to_write)


if __name__ == '__main__':
  # run the practice tracker script
  live_practice_tracker(path, filename, topics)
