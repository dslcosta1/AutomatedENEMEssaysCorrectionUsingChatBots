from utils.model_setup import *
from utils.dataset_setup import *
from utils.experiment_setup import *
from utils.save_results import *
from utils.state_control import *
import gc
import random


def execute_experiment(state, model_identifier, path_to, round_api_key = -1, excution_beggining = 0) :
    path_to_experiments = "./experiments/"
    """
    Setup Model
    """
    model_name, model_code = choose_model(state['Model'])
    chat = model_setup(model_name, round_api_key)

    """
    Setup Dataset
    """
    dataset_name, dataset_code = setup_dataset(state['Database'])
    essays_dataset = getDataset(path_to, dataset_name)

    while state['Experimento'] <= 6:
        """
        Setup Experiment
        """
        experiment_name, experiment_code = choose_experiment(state['Experimento'])
        exp = setup_experiment(path_to_experiments, experiment_name)
        
        new_udpates = {
            'Model': model_code,
            'Database': dataset_code,
            'Experimento': experiment_code,
        }
        print(state)
        state = update_state(state, new_udpates)
        print(state)
        save_state(state, path_to, model_identifier)
        
        while state['Execucao'] <= state['MaxExecucao']:
            print()
            print()
            print("Execution number: " + str(state['Execucao']))
            print()
            print()
            
            start = state['Batch']
            path_to_save = create_experiment_folder(path_to, model_name, experiment_name, dataset_name)
            filename_to_save = build_filename_to_save(model_name, experiment_name, dataset_name, str(state['Execucao']))
            
            batch = 2
            limit = len(essays_dataset)
            
            run_experiment(exp, essays_dataset, start, limit, batch, path_to_save, filename_to_save, model_name, chat, state, path_to, dataset_name, model_identifier, round_api_key)
            
            '''
            Change to new execution
            '''
            new_state = {
                'Execucao': state['Execucao'] + 1,
                'Batch': 0
            }
            state = update_state(state, new_state)
            save_state(state, path_to, model_identifier)
    
        '''
        Change to new experiment
        '''
        new_state = {
            'Execucao': excution_beggining,
            'Experimento': state['Experimento'] + 1,
            'Batch': 0
        }
        state = update_state(state, new_state)
        save_state(state, path_to, model_identifier)

def run_experiment(exp, essays_dataset, start, limit, batch, path_to_save, filename_to_save, model_name, chat, state, path_to, dataset_name, model_identifier, round_api_key):
    end = start
    key_id = random.randint(1, 5)
    for ini in range(start, limit-batch, batch):
        end = ini + batch
        del chat
        gc.collect()
        chat = model_setup(model_name, key_id%5 + 1)
        try:
            essays_outputs = run_model(essays_dataset, exp, ini, end, model_name, chat, dataset_name)
            if (round_api_key == -1):
                key_id += 1
                del chat
                gc.collect()
                chat = model_setup(model_name, key_id%5 + 1)
        except Exception as e:
            print(f"There was an exception on run_experiment!!: {e}")
            time.sleep(1)
            key_id += 1
            del chat
            gc.collect()
            chat = model_setup(model_name, key_id%5 + 1)
            essays_outputs = run_model(essays_dataset, exp, ini, end, run_model, chat, dataset_name)
        
        if ini == 0:
            create_csv_header(path_to_save, filename_to_save, essays_outputs[0].keys())
        
        save_data(path_to_save, filename_to_save, essays_outputs)
        
        print("Processed essays from " + str(ini) + " to: " + str(end))
        new_state = {
            'Batch': end
        }
        state = update_state(state, new_state)
        save_state(state, path_to, model_identifier)

    print("End value is: ", end)
    print("Limit value is:", limit)

    if limit !=  end:
        essays_outputs = run_model(essays_dataset, exp, end, limit, model_name, chat, dataset_name)
        save_data(path_to_save, filename_to_save, essays_outputs)
        print("Processed essays from " + str(end) + " to: " + str(limit))