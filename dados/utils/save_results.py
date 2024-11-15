import csv
import os

"""
Writing CSV with results
"""
def create_csv_header(path_to, filename, fields):
  file_path = path_to + filename + ".csv"

  with open(file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

def save_data(path_to, filename, essays_outputs):
  file_path = path_to + filename + ".csv"

  with open(file_path, mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=essays_outputs[0].keys())
    writer.writerows(essays_outputs)


"""
Defining folder to salve the experiment results
"""
def create_folder(path_to, folder_name):
  # Path to the folder
  folder_path = path_to + folder_name

  # Check if the folder exists
  if not os.path.exists(folder_path):
      # Create the folder if it doesn't exist
      os.makedirs(folder_path)
      print(f"Folder '{folder_path}' created.")
  else:
      print(f"Folder '{folder_path}' already exists.")

  return folder_path + "/"


def create_experiment_folder(path_to, model_name, experiment_name, dataset_name):
  model_folder_path = create_folder(path_to + "results/", model_name)
  experiment_model_folder_path = create_folder(model_folder_path  , experiment_name)
  dataset_experiment_model_folder_path = create_folder(experiment_model_folder_path , dataset_name)

  return dataset_experiment_model_folder_path


"""
Defining filename to salve the experiment results
"""
def build_filename_to_save(model_name, experiment_name, dataset_name, id="##"):
  filename_to_save = dataset_name + "-" + model_name + "-" + experiment_name
  if id == '##':
    id = ""
    id = input("O nome to arquivo de output será: " + filename_to_save + ". Adicione um disambiguador: ")
  filename_to_save += "-" + id
  print("CSV with the answer will be saved in: " + filename_to_save)

  return filename_to_save