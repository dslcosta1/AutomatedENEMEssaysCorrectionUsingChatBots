import random
import csv
import os



REDACAO_NOTA_MIL = "essaysFullGrade" # Dataset with all essays with maximum grade available online
REDACAO_TOTAL = "aes_enem_dataset" #
REDACAO_TOTAL_COM_TREINO_E_VALIDACAO = "propor2024"
REDACAO_EXTENDIDO_PROPOR_E_NOTA_COMPLETA = "extended2024"
REDACAO_EXTENDIDO_PROPOR_E_NOTA_COMPLETA_COM_TREINO_E_VALIDACAO = "extended_complete"


def setup_dataset(dataset_cod = -1):

  if dataset_cod == -1:
    print("ATENCAO - Escolha o dataset:")
    print("1 - " + REDACAO_NOTA_MIL)
    print("2 - " + REDACAO_TOTAL)
    print("3 - " + REDACAO_TOTAL_COM_TREINO_E_VALIDACAO)
    print("4 - " + REDACAO_EXTENDIDO_PROPOR_E_NOTA_COMPLETA)
    print("5 - " + REDACAO_EXTENDIDO_PROPOR_E_NOTA_COMPLETA_COM_TREINO_E_VALIDACAO)
    print("6 - Outro")
    dataset_cod = int(input("Coloque o número do dataset que gostaria de executar: "))
  dataset_name = ""

  match dataset_cod:
    case 1:
      dataset_name = REDACAO_NOTA_MIL
    case 2:
      dataset_name = REDACAO_TOTAL
    case 3:
      dataset_name = REDACAO_TOTAL_COM_TREINO_E_VALIDACAO
    case 4:
      dataset_name = REDACAO_EXTENDIDO_PROPOR_E_NOTA_COMPLETA
    case 5:
      dataset_name = REDACAO_EXTENDIDO_PROPOR_E_NOTA_COMPLETA_COM_TREINO_E_VALIDACAO
    case _:
      dataset_name = input("Digite o nome do dataset: ")

  print("Dataset escolhido: " + dataset_name)
  return dataset_name, dataset_cod


def getDataset(path_to, dataset_name):
  output = []
  match dataset_name:
    case "essaysFullGrade":
      essays_data = []

      filepath = path_to + "Datasets/fullGradeEnemEssays2024/test.csv"
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)

      output = essays_data
    case "aes_enem_dataset":
      essays_data = []

      filepath = path_to + "Datasets/propor2024/test.csv"
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)

      output = essays_data
    case "propor2024":
      essays_data = []

      filepath = path_to + "Datasets/" + dataset_name + '/train.csv'
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)
      print(f"Propor2024 train size = {len(essays_data)}")

      filepath = path_to + "Datasets/" + dataset_name + '/test.csv'
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)
      print(f"Propor2024 train and validation size = {len(essays_data)}")

      filepath = path_to + "Datasets/" + dataset_name + '/validation.csv'
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)

      print(f"Propor2024 total size = {len(essays_data)}")
      output = essays_data

    case "extended2024":
      essays_data = []

      filepath = path_to + "Datasets/propor2024/test.csv"
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)

      filepath = path_to + "Datasets/fullGradeEnemEssays2024/test.csv"
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)

      output = essays_data

    case "extended_complete":
      essays_data = []

      filepath = path_to + "Datasets/propor2024/train.csv"
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)

      filepath = path_to + "Datasets/propor2024/test.csv"
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)

      filepath = path_to + "Datasets/propor2024/validation.csv"
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)

      filepath = path_to + "Datasets/fullGradeEnemEssays2024/train.csv"
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)

      filepath = path_to + "Datasets/fullGradeEnemEssays2024/test.csv"
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)

      filepath = path_to + "Datasets/fullGradeEnemEssays2024/validation.csv"
      with open(filepath, mode ='r') as file:
            csvFile = csv.DictReader(file)
            for lines in csvFile:
                essays_data.append(lines)

      output = essays_data

  random.seed(0)
  random.shuffle(output)
  return output