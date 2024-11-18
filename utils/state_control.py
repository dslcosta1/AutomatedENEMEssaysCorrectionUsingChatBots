import csv

STATE_FILENAME = "EstadoExperimentosChat_"

def create_state(model_code, dataset_code, experiment_code, execution, execution_limit, batch_saved):
    state = {
        'Model': model_code,
        'Database': dataset_code,
        'Experimento': experiment_code,
        'Execucao': execution,
        'MaxExecucao': execution_limit,
        'Batch': batch_saved
    }
    
    return state


def update_state(state, new_values):
    state.update(new_values)
    return state


def save_state(state, path_to, model_identifier):
    
  with open(path_to + STATE_FILENAME + model_identifier + ".csv", mode='w') as file:
    print("Saving state: " + str(state))
    writer = csv.DictWriter(file, fieldnames=state.keys())
    writer.writeheader()
    writer.writerow(state)


def retrieve_state(path_to, model_identifier):
    state_read = None
    
    with open(path_to + STATE_FILENAME + model_identifier + ".csv", mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            state_read = row  # Each row is a dictionary
        
        if state_read is None:  # Handle case where no rows exist in the file
            raise ValueError("The file is empty or does not contain valid data.")
        
    new_state = {}
    for key in state_read.keys():
        new_state[key] = int(state_read[key])
    print(new_state)
    return new_state