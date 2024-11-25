import re
import numpy as np
from sklearn.metrics import cohen_kappa_score


QWK = "QWK"
RMSE = "RMSE"
MAE = "MAE"

def choose_metric():
    print("ATENCAO - Escolha a metrica:")
    print("1 - " + QWK)
    print("2 - " + RMSE)
    print("3 - " + MAE)
    print("4 - other")
    metric_cod = int(input("Coloque o número do modelo que gostaria de executar: "))
    metric_name = ""
    
    match metric_cod:
        case 1:
            metric_name = QWK
        case 2:
            metric_name = RMSE
        case 3:
            metric_name = MAE
        case _:
            print("Métrica inválida, escolha um novo:")
            choose_metric()
    
    return metric_name

def fix_grade(grade):
    possible_grades = [0, 40, 80, 120, 160, 200]
    mais_proxima = -1
    dif = 1000
    for possible_grade in possible_grades:
        if abs(grade - possible_grade) < dif:
            mais_proxima = possible_grade
            dif = abs(grade - possible_grade)
    return mais_proxima

def pegar_nota(grades_list, ind, has_fix_grade=False):
    new_grade = []
    for grade in grades_list:
        if not (isinstance(grade, list) or isinstance(grade, tuple)):
            print("Skiping essay with grade: " + str(grade))  
        else:
            if has_fix_grade:
                new_grade.append(fix_grade(grade[ind]))
            else:
                new_grade.append(grade[ind])
    return new_grade

def get_grades(dataset, model_name):
    model_grade_key = model_name.split("-")[0] + "_grades"
    
    nota_original = []
    nota_gemini = []
    for index, (original, gemini) in enumerate(zip(dataset['grades'], dataset[model_grade_key])):
        try:
            o = eval(original)
        except:
            clean_original = re.sub(r'\s+', ' ', original)
            remove_brackets = clean_original.replace('[ ', '[').replace(' ]', ']').replace(' ', ', ').replace('(', '[').replace(')', ']')
            o = eval(remove_brackets)
        g = eval(gemini)
        nota_original.append(o)
        nota_gemini.append(g)
    
    return nota_original, nota_gemini

def calculate_qwk(nota_original, nota_model):
    results = []
    for indice in range(0, 5):
        y = pegar_nota(nota_original, indice, True)
        y_hat = pegar_nota(nota_model, indice, True)
        
        qwk = cohen_kappa_score(y, y_hat, weights='quadratic', labels=[0, 40, 80, 120, 160, 200])
        results.append(qwk)
        
    return results


def calculate_rmse(nota_original, nota_model):
    results = []
    for indice in range(0, 5):
        y = np.array(pegar_nota(nota_original, indice, True))
        y_hat = np.array(pegar_nota(nota_model, indice, True))
        
        # Calculate the squared differences
        squared_diff = (y - y_hat) ** 2
        
        # Compute the mean of squared differences
        mean_squared_diff = np.mean(squared_diff)
        
        # Take the square root of the mean squared difference
        rmse = np.sqrt(mean_squared_diff)
        
        print(f"RMSE: {rmse}")
        
        results.append(rmse)
    
    return results


def calculate_mae(nota_original, nota_model):
    results = []
    for indice in range(0, 5):
        y = np.array(pegar_nota(nota_original, indice, True))
        y_hat = np.array(pegar_nota(nota_model, indice, True))
        
        # Calculate the absolute differences
        absolute_diff = np.abs(y - y_hat)
        
        # Compute the mean of absolute differences
        mae = np.mean(absolute_diff)
        
        print(f"MAE: {mae}")
        
        results.append(mae)
    
    return results