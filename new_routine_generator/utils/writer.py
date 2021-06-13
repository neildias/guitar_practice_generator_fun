import pandas as pd
import os
from utils.default_params import main_file_name, record_log, todays_full_date
from datetime import datetime
import xlsxwriter


today = datetime.now()  # use time at the time of writing the file

def create_newfile():
  """
  A simple function to generate response from the user.
  :return: bool
  """
  response = input("\nIf you have ensured the file is writable press enter, "
                   "OR to create a new Excel type new filename OR to use the "
                   "existing file_name with a suffix type 1 ")
  #print(f"Creating a new file with name as {response} to store practice data")
  return response


def create_new_filename(original_filename: str,
                        user_response: str):
  """
  Creates new file name depending on the users response

  :param original_filename: str
  :param user_response: str
  :return: str | new filename
  """
  if user_response == "1":
    time = str(today.time())[:8].replace(":","_")
    date = str(today.date()).replace("-","_")
    print(time)
    new_filename = f"{original_filename}_{date}_{time}.xlsx"
  else:
    new_filename = f"{user_response}.xlsx"
  return new_filename


def formatter(df,workbook_object, sheet_object, highlight_val: int):
  """
  Uses Xlwriter library to do formatting of cell width, conditional formatting
  :param worksheet:
  :param sheet_object:
  :return:
  """
  # set cell width
  sheet_object.set_column(0, 0, 19)  # date col
  sheet_object.set_column(1, 200, 2.71) # rest of the cols

  # 2 formatting
  # rotate column headers
  # works at cell level
  cell_format = workbook_object.add_format()
  cell_format.set_rotation(90)
  counter = 1
  for col_name in df.columns.tolist():
                      # row, col, text, format
    sheet_object.write(0, counter, col_name, cell_format)
    counter += 1

  # 3rd formatting
  # highlight entries higher than given value
  # works at sheet level
  # green if greater than highlight_val
  cond_format = workbook_object.add_format()
  cond_format.set_font_size(14)
  cond_format.set_bold()
  cond_format.set_underline()
  cond_format.set_pattern(0)
  cond_format.set_bg_color('#99FF99')
  # frow,fcol,lrow,lcol
  sheet_object.conditional_format(1, 1, 2000, 200, {'type': 'cell',
                                             'criteria': '>=',
                                             'value': highlight_val,
                                             'format': cond_format})



def write_excel(path: str,
                filename: str,
                *dfs,
                highlight_val: int,
                include_date:bool):
  """
  writes 3 dataframes to 3 sheets in an existing excel file (or creates one).

  :param path: str
  :param filename: str
  :param dfs: dataframes | tuple of three dataframes
  :return:
  """
  if ".xlsx" in filename and include_date:
    filename = filename[:-5]
    full_path = f"{path}{filename}_{todays_full_date}.xlsx"
  else:
    full_path = path + filename
  df1, df2, df3, df4, df5 = dfs
  # rename filename and path if file name provided is too long

  if len(full_path) > 200:
    print("\nWARNING!!!")
    print(f"\nPath and filename exceed 200 characters. {full_path}")
    print("\nSaving file on the desktop with the name as first 100 characters")
    path = "C:\\Users\\Neil\Desktop\\"
    filename = filename[:100] + ".xlsx"

  with pd.ExcelWriter(full_path, engine='xlsxwriter') as writer:

    df1.to_excel(writer, sheet_name="Time_Log")
    df2.to_excel(writer, sheet_name="Tempo")
    df3.to_excel(writer, sheet_name="Notation")
    df4.to_excel(writer, sheet_name="Notes")
    df5.to_excel(writer, sheet_name="Today")
    print(f"\nSUCCESS! Dataframe values stored in {path + filename}")

    try: # some minimilist formatting
      workbook = writer.book
      tl_log = writer.sheets['Time_Log']
      tempo_ = writer.sheets['Tempo']
      notation_ = writer.sheets['Notation']
      my_notes = writer.sheets['Notes']
      todays_ = writer.sheets['Today']
      for sheet in [tl_log, tempo_, notation_, my_notes, todays_]:
        if sheet in [my_notes, todays_]:
          sheet.set_column(0, 200, 50)
        else:
          formatter(df2, workbook, sheet, highlight_val)

      print("Formatting successfully applied!")

    except Exception as e:
      print(e)

  with open(path+record_log, "a+") as f:
    f.writelines(todays_full_date+"\n")


def data_to_excel(path: str,
                  filename: str,
                  *dfs: "DataFrame",
                  highlight_val: int = 5,
                  date_in_name: bool = True):
  """
  Creates excel with 5 sheets from the given dataframes
  :param path:
  :param filename:
  :param dfs:
  :param date_in_name:
  :return:
  """
  assert len(dfs) == 5, "Please pass only 5 pandas dataframes"
  default_filename = filename[:-5] # remove extension

  # exit program if path is invalid
  if not os.path.exists(path):
    print(f"\nERROR! Directory disconnected. Cannot save data to the path "
          f"{path}.")
    return

  while True:
    try:
      # writing to the main file
      write_excel(path,
                  main_file_name,
                  *dfs,
                  highlight_val=highlight_val,
                  include_date=date_in_name)
      break

    except PermissionError:
      print("\nERROR! Encountered Permission Error. Please ensure the file is "
            "closed or writable.")

    except Exception as e:
      print(f"\nERROR! Encountered {e}. Please ensure the file is closed or "
            f"writable.")

    # resolve the exceptions
    user_input = create_newfile()
    if not user_input:
      print("\nNo input received. Attempting to write on the file again.\n")
      continue
    else:
      filename = create_new_filename(default_filename, user_input)
