from utils.model_setup import *
from utils.dataset_setup import *
from utils.experiment_setup import *
from utils.save_results import *
from utils.state_control import *
from utils.run_experiment import *

from importlib import reload

model_identifier = 'llama'
path_to = "./data/"
api_key = 1 # With value -1 it will change every 10 iterations


"""
Setup State
"""
use_experiment_state = True

state = create_state(-1, -1, -1, 1, 5, 0)
if use_experiment_state:
  state = retrieve_state(path_to, model_identifier)


"""
Setup State
"""
execute_experiment(state, model_identifier, path_to, api_key)