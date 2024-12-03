EXPERIMENT_1 = "exp1"
EXPERIMENT_2 = "exp2"
EXPERIMENT_3 = "exp3"
EXPERIMENT_4 = "exp4"
EXPERIMENT_5 = "exp5"
EXPERIMENT_6 = "exp6"
EXPERIMENT_7 = "exp7"


def choose_experiment(experiment_cod = -1):

  if experiment_cod == -1:
    print("ATENCAO - Escolha o Experimento:")
    print("1 - " + "experimento1")
    print("2 - " + "experimento2")
    print("3 - " + "experimento3")
    print("4 - " + "experimento4")
    print("5 - " + "experimento5")
    print("6 - " + "experimento6")
    print("7 - " + "experimento7")
    print("8 - Outro")
    experiment_cod = int(input("Coloque o número do experimento que gostaria de executar: "))

  experiment_name = ""

  match experiment_cod:
    case 1:
      experiment_name = EXPERIMENT_1
    case 2:
      experiment_name = EXPERIMENT_2
    case 3:
      experiment_name = EXPERIMENT_3
    case 4:
      experiment_name = EXPERIMENT_4
    case 5:
      experiment_name = EXPERIMENT_5
    case 6:
      experiment_name = EXPERIMENT_6
    case 7:
      experiment_name = EXPERIMENT_7
    case _:
      print("Valor invalido do experimento")
      setup_experiment()


  print("Experimento escolhido: " + experiment_name)
  return experiment_name, experiment_cod


def setup_experiment(path_to_experiment_prompts, experiment_name):
  return Experimento(path_to_experiment_prompts, experiment_name)


class Experimento:
  prompt_template = ""

  def __init__(self, path_to_experiment_prompts, experiment_name):
    self.prompt_template = read_experiment_prompt(path_to_experiment_prompts, experiment_name)
    print("Create " + experiment_name)
    print("Prompt template: \n" + self.prompt_template)

  def build_prompt(self, essay, prompt, supporting_text):
    filled_prompt = self.prompt_template.replace('<TEMA>', prompt).replace('<SUPORTE>', supporting_text).replace('<REDAÇÃO>', essay)
    return filled_prompt

def read_experiment_prompt(path_to_experiment_prompts, experiment_name):
  f = open(path_to_experiment_prompts + experiment_name + ".txt", "r")
  return f.read()