import pandas as pd
import os
from utils.default_params import record_log, todays_full_date
from datetime import datetime


today = datetime.now()  # use time at the time of writing the file


def create_new_file():
  """
  A simple function to generate response from the user.
  
  :return: bool
  """
  response = input("\nIf you have ensured the file is writable press enter, "
                   "OR to create a new Excel type new filename OR to use the "
                   "existing file_name with a suffix type 1 ")
  
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
    time = str(today.time())[:8].replace(":", "_")
    date = str(today.date()).replace("-", "_")
    print(time)
    new_filename = f"{original_filename}_{date}_{time}.xlsx"
  
  else:
    new_filename = f"{user_response}.xlsx"
  
  return new_filename


# excel formatting functions
def _set_column_value_validator(tuple_of_values: tuple):
  """
  to be used excel formatter functions
  
  :param tuple_of_values: tuple or list-like objects
  :return:
  """
  
  assert pd.api.types.is_list_like(
          tuple_of_values
  ), "formatter expects a list-like object, got {type(tuple_of_values)}, " \
     f"{tuple_of_values} "
  
  assert len(tuple_of_values) == 3, f"formatter expects 3 values, got " \
                                    f"{tuple_of_values}"
  
  for value in tuple_of_values:
    assert ((isinstance(value, int) or
             isinstance(value, float))), "formatter expects ints, got " \
                                         "{type(value)}, {value}"


def column_width_setter(sheet_object, *set_column_args: tuple):
  """
  Helps set column width of the excel file
  
  :param sheet_object:
  :param set_column_args:
  :return:
  """
  
  # does nothing if an empty tuple is passed
  if len(set_column_args) >= 1:
    for row_col_value in set_column_args:
      _set_column_value_validator(row_col_value)
      sheet_object.set_column(*row_col_value)


def alignment_border_formatter(workbook_object: pd.ExcelWriter,
                               sheet_obj: pd.ExcelWriter,
                               first_col: int = 0,
                               last_col: int = 20,
                               width: float = 20.):
  """
  Basic formatting of setting no borders and left aligning
  
  :param workbook_object: pd.ExcelWriter
  :param sheet_obj: pd.ExcelWriter
  :param first_col: int
  :param last_col: int
  :param width: float
  :return:
  """
  
  cell_format = workbook_object.add_format(
          {'bold': True,
           'align': "left",
           'valign': "vcenter",
           'border': None,
           # 'num_format': 'mmm d yyyy hh:mm AM/PM',
           }
  )
  # cell_format.set_border('none')  # no border
  # cell_format.set_align("left")
  # cell_format.set_align("vcenter")
  
  sheet_obj.set_column(first_col,  # first col
                       last_col,  # last col
                       width,  # width
                       cell_format)
  
  # Write the column headers with the defined format.
  # for col_num, value in enumerate(df.columns.values):
  #   sheet_obj.write(0, col_num + 1, value, cell_format)
  #
  # writer.save()


def formatter(df: pd.DataFrame,
              workbook_object: pd.ExcelWriter,
              sheet_object: pd.ExcelWriter,
              highlight_val: int):
  """
  Uses Xlwriter library to do formatting of cell width, conditional formatting
  
  :param df:
  :param workbook_object:
  :param sheet_object:
  :param highlight_val:
  :return:
  """
  
  # 1st formatting
  # rotate column headers
  # works at cell level
  cell_format = workbook_object.add_format()
  cell_format.set_rotation(90)
  counter = 1
  
  for col_name in df.columns.tolist():
    # row, col, text, format
    sheet_object.write(0, counter, col_name, cell_format)
    counter += 1
  
  # 2nd formatting
  # highlight entries higher than given value
  # works at sheet level
  # green if greater than highlight_val
  cond_format = workbook_object.add_format()
  cond_format.set_font_size(14)
  cond_format.set_bold()
  cond_format.set_underline()
  cond_format.set_pattern(0)
  cond_format.set_bg_color('#99FF99')
  
  sheet_object.conditional_format(1,       # first row,
                                  1,       # first column,
                                  2000,    # last row,
                                  200,     # last column
                                  {'type': 'cell',
                                   'criteria': '>=',
                                   'value': highlight_val,
                                   'format': cond_format})


def write_excel(path: str,
                filename: str,
                *dfs: pd.DataFrame,
                highlight_val: int,
                include_date: bool):
  """
  writes 5 dataframes to 5 sheets in an existing excel file (or creates one).
  
  :param path: str
  :param filename: str
  :param dfs: pd.Dataframe
  :param highlight_val: int
  :param include_date: bool
  :return: bool | True if successful in writing excel else False
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
    
    path = "C:\\Users\\Neil\\Desktop\\"
    
    filename = filename[:100] + ".xlsx"
  
  with pd.ExcelWriter(full_path, engine='xlsxwriter') as writer:
    
    try:
      df1.to_excel(writer, sheet_name="Time_Log")
      df2.to_excel(writer, sheet_name="Tempo")
      df3.to_excel(writer, sheet_name="Notation")
      df4.to_excel(writer, sheet_name="Notes")
      df5.to_excel(writer, sheet_name="Today")
      print(f"\nSUCCESS! Dataframe values stored in {path + filename}")
      
    except Exception as e:
      print(f"Writing to the excel file failed. {e}")
      return False
    
    # some minimalist formatting
    try:
      workbook = writer.book
      
      # get sheet objects
      tl_log_ = writer.sheets['Time_Log']
      tempo_ = writer.sheets['Tempo']
      notation_ = writer.sheets['Notation']
      my_notes_ = writer.sheets['Notes']
      today_ = writer.sheets['Today']
      
      sheets = [tl_log_, tempo_, notation_, my_notes_, today_]
      
      for sheet in sheets:
        
        if sheet in [my_notes_, today_]:
          
          if sheet is today_:
            row_col_val_today = (0, 20, 20)
            
            column_width_setter(sheet, row_col_val_today)
            alignment_border_formatter(workbook, sheet)
          
          else:
            row_col_val_notes = (
                    (0, 0, 19),  # date col
                    (1, 1, 50),  # lessons col
                    (2, 2, 100),  # Notes col
            )
            
            column_width_setter(sheet, *row_col_val_notes)
        
        else:
          
          row_col_val_others = (
                  (0, 0, 19),
                  (1, 200, 3)
          )
          
          column_width_setter(sheet, *row_col_val_others)
          formatter(df2, workbook, sheet, highlight_val)
      
      print("Formatting successfully applied!")
    
    except Exception as e:
      print(e)
      print("Formatting Failed!")
  
  with open(path + record_log, "a+") as f:
    f.writelines(todays_full_date + "\n")
    
  return True


def data_to_excel(path: str,
                  filename: str,
                  *dfs: pd.DataFrame,
                  highlight_val: int = 5,
                  date_in_name: bool = True):
  """
  Creates excel with 5 sheets from the given dataframes
  
  :param path: str
  :param filename: str
  :param dfs: pd.DataFrame
  :param highlight_val: int
  :param date_in_name: bool
  :return: bool | True if successful else False
  """
  
  assert len(dfs) == 5, "Please pass only 5 pandas dataframes"
  
  # exit program if path is invalid
  if not os.path.exists(path):
    print(f"\nERROR! Directory disconnected. Cannot save data to the path "
          f"{path}.")
    return False
  
  while True:
    try:
      # writing to the main file
      write_excel(path,
                  filename,
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
    user_input = create_new_file()
    
    if not user_input:
      print("\nNo input received. Attempting to write on the file again.\n")
      continue
    
    else:
      new_filename = create_new_filename(filename, user_input)
      filename = new_filename
  
  return True
