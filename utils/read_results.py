import pandas as pd

def read_csv(path_to, filename_to_save):
  df = pd.read_csv(path_to + filename_to_save + ".csv")
  return df