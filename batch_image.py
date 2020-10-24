'''
Batches files based on extension type into folders.

python batch_image.py --folder_path=/Users/<user>/Desktop/folder_name --test_mode=on
'''

import argparse
import os
from os.path import isfile, join, exists
import string
import csv

def get_non_csv_files(cwd):
  """Finds files that are not of type csv.

    Args:
        cwd (string): The current working directory.

    Returns:
        The list of non csv files.
    """
  only_files = [f for f in os.listdir(cwd) if isfile(join(cwd, f))]
  only_visible_files =
      filter(lambda file: not(file.startswith('.')), only_files)
  only_visible_files_non_csv =
      filter(lambda file: not(file.endswith('.csv')), only_visible_files)
  return only_visible_files_non_csv

def get_csv_file(cwd):
  """Finds files that are of type csv.

    Args:
        cwd (string): The current working directory.

    Returns:
        The first of the csv files.
    Throws if no csv file is found.
    """
  only_files = [f for f in os.listdir(cwd) if isfile(join(cwd, f))]
  only_visible_files =
      filter(lambda file: not(file.startswith('.')), only_files)
  only_csv_files = filter(lambda file: file.endswith('.csv'), only_files)
  if(len(only_csv_files) > 0):
    return only_csv_files[0]
  else:
    raise Exception('Error: No CSV file found in this folder.') 

def get_custom_input(question, the_type, answers_list):
  """Requests input from the user.

    Converts the input into the specified type. Checks the input answer against
    the answers in the answer_list (if a list is provided). 

    Args:
        question (int): The first parameter.
        the_type (type): The second parameter.
        answers_list (list<any>|None): The list of possible answers or None if
            any answer is accepted.

    Returns:
        The answer the user provided, assuming it is valid.
    Throws if the answer_list does not contain the user's answer.
    """
  answer = the_type(raw_input('> {q}: '.format(q=question)))
  if(answers_list is None):
    return answer
  if(the_type is int and answer in answers_list):
    return answer
  if(the_type is str and answer.lower() in answers_list):
    return answer.lower()
  else:
    raise Exception(
      'Error: {ans} is not a valid answer. Exiting program'.format(ans=answer)) 

def create_alphabet_map():
  """Creates a map of letters to numbers
  
  returns dict.
  """
  map = dict()
  for index, letter in enumerate(string.ascii_lowercase):
    map[letter] = index
  return map

def read_csv(csv_file_name, col_index, has_header):
  image_names = []
  with open(csv_file_name, 'rb',) as csv_file:
    reader = csv.reader(csv_file, delimiter=',', quotechar='|')
    for index, row in enumerate(reader):
      if index is 0 and has_header:
        continue
      image_name = row[col_index]
      if image_name:
        image_names.append(image_name)
    return image_names

def get_full_path(start_path, end_path):
  """Concats two paths together seperated by the OS seperator."""
  return '{start_path}{sep}{end_path}'.format(
    start_path=start_path, sep=os.path.sep, end_path=end_path)

def create_dir(path):
  """Creates a directory from a specified path.

    Args:
        path (int): A string representation of the path to create the dir.

    Returns: The path
    Throws if the creation of the directory was unsuccessful.
    """
  try:
    os.mkdir(path)
  except OSError:
    print ("Creation of the directory %s failed" % path)
  else:
    print ("Successfully created the directory %s " % path)
    return path

def setup_args():
  """Creates the arguments for the application.

    Returns: The parsed args.
    """
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--folder_path', type=str,
                   help='The folder path where the images are.')
  parser.add_argument('--test_mode', type=str, default='on',
                   help='Whether to run in test mode or not. In test mode, no files are moved.')

  return parser.parse_args()

def move_files(image_names, batch_num, file_extension, is_test_mode):
  current_batch_index = 0
  batches_created = 0
  current_batch_directory = None
  for index, file_name in enumerate(image_names):
    if current_batch_index >= batch_num or current_batch_directory is None:
      current_batch_index = 1
      batches_created += 1
      new_folder_name = "batch_{num}".format(num = batches_created)
      current_batch_directory = get_full_path(os.getcwd(), new_folder_name)
      if not(is_test_mode):
        create_dir(current_batch_directory)
    else:
      current_batch_index += 1
    full_file_name = 
        "{file_name}.{ext}".format(file_name = file_name, ext = file_extension)
    image_file_path = get_full_path(os.getcwd(), full_file_name)
    if isfile(image_file_path):
        new_file_path = current_batch_directory + os.path.sep + full_file_name
        if is_test_mode:
          print "Test mode on - Would move '{a}' to '{b}'".format(a=image_file_path, b=new_file_path)
        else:
          os.rename(image_file_path, new_file_path)
    else:
      print "Warning: Couldn't find file '{f}'".format(f=full_file_name)

def main():
  """
    Requests the required info from the user.
    Pulls the data from a column in a spreadsheet and iterates over the files
        in the folder to find files named with the data from rows in the
        spreadsheet.
    Uses the batch number provided by the user to create folders and place as
        many found files into those folders as specified.
    """
  args = setup_args()
  is_test_mode = False if args.test_mode.lower() == 'off' else True
  folder_path = args.folder_path
  if folder_path is None:
    raise Exception("No folder argument provided. Please add --folder_path=path when running script.")
  print("Starting batch_image script - test mode is {val}".format(val=is_test_mode))
  print("")

  if exists(folder_path):
    os.chdir(folder_path)
  else:
    raise Exception("No folder path exists: {path}".format(path=folder_path))
  cwd = os.getcwd()
  csv_file_name = get_csv_file(cwd)
  print("Found csv file: {f}".format(f=csv_file_name))
  only_visible_files_non_csv = get_non_csv_files(cwd)
  print("Found {num} other files to be batch moved"
      .format(num=len(only_visible_files_non_csv)))
  print("")


  batch_num = get_custom_input(
    "How many images should be placed into a folder (please enter between 1-500)",
    int, range(1, 501))
  column_name = get_custom_input(
    "What column is the data in (please enter between A-Z)",
    str, list(string.ascii_lowercase))
  has_header = get_custom_input(
    "Does column {col} have a header? (please enter Y/N)"
        .format(col=column_name),
    str, ["y", "n"])
  file_extension = get_custom_input(
    "What is the extension type of the files? (jpg, jpeg, png, mp3, etc)"
        .format(col=column_name),
    str, None)
  if str(file_extension) == "":
    raise Exception("Must provide a file extension type.")

  print("")

  col_index = create_alphabet_map()[column_name]
  image_names = read_csv(csv_file_name, col_index, has_header)
  move_files(image_names, batch_num, file_extension, is_test_mode)


if __name__ == "__main__":
  main()