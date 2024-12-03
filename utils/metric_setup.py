import re
import numpy as np
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from scipy.stats import spearmanr

QWK = "QWK"
RMSE = "RMSE"
MAE = "MAE"
R2 = "R2"

def choose_metric():
    print("ATENCAO - Escolha a metrica:")
    print("1 - " + QWK)
    print("2 - " + RMSE)
    print("3 - " + MAE)
    print("4 - " + R2)
    print("6 - other")
    metric_cod = int(input("Coloque o número do modelo que gostaria de executar: "))
    metric_name = ""
    
    match metric_cod:
        case 1:
            metric_name = QWK
        case 2:
            metric_name = RMSE
        case 3:
            metric_name = MAE
        case 4:
            metric_name = R2
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

        try:
            g = eval(gemini)
        except:
            clean_original = re.sub(r'\s+', ' ', gemini)
            remove_brackets = clean_original.replace('[ ', '[').replace(' ]', ']').replace(' ', ', ').replace('(', '[').replace(')', ']')
            g = eval(remove_brackets)
        
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
                
        results.append(rmse)
    
    return results

def calculate_abs_diff(nota_original, nota_model):
    results = []
    for indice in range(0, 5):
        y = np.array(pegar_nota(nota_original, indice, True))
        y_hat = np.array(pegar_nota(nota_model, indice, True))
        
        # Calculate the absolute differences
        absolute_diff = np.abs(y - y_hat)

        results.append(absolute_diff)
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
                
        results.append(mae)
    
    return results

def calculate_r2(nota_original, nota_model):
    results = []
    for indice in range(0, 5):
        y = np.array(pegar_nota(nota_original, indice, True))
        y_hat = np.array(pegar_nota(nota_model, indice, True))
        
        # Calculate R² score
        r2 = r2_score(y, y_hat)
                
        results.append(r2)
    
    return results

def calculate_spearmanr(nota_original, nota_model):
    results = []
    for indice in range(0, 5):
        y = np.array(pegar_nota(nota_original, indice, True))
        y_hat = np.array(pegar_nota(nota_model, indice, True))
        
        # Calculate Spearman Rank Correlation Coefficient
        coef, p_value = spearmanr(y, y_hat)
                
        results.append(coef)
        
    return results

def calculate_mape(nota_original, nota_model):
    results = []
    for indice in range(0, 5):
        y = np.array(pegar_nota(nota_original, indice, True))
        y_hat = np.array(pegar_nota(nota_model, indice, True))
        
        # Avoid division by zero by replacing zeros with a very small number
        y = np.where(y == 0, np.finfo(float).eps, y)
        
        # Calculate the absolute percentage differences
        percentage_diff = np.abs((y - y_hat) / y)
        
        # Compute the mean of percentage differences
        mape = np.mean(percentage_diff) * 100  # Convert to percentage
                
        results.append(mape)
    
    return results

def calculate_pia(nota_original, nota_model, tolerancia=80):
    """
    Calcula a Precisão do Intervalo Absoluto (PIA) para cada conjunto de notas.

    Args:
        nota_original: Notas verdadeiras.
        nota_model: Notas preditas pelo modelo.
        tolerancia: Intervalo de tolerância para considerar a predição como precisa.

    Returns:
        Lista de valores PIA para cada conjunto de notas.
    """
    results = []
    for indice in range(0, 5):
        y = np.array(pegar_nota(nota_original, indice, True))
        y_hat = np.array(pegar_nota(nota_model, indice, True))
        
        # Calculate the absolute differences
        absolute_diff = np.abs(y - y_hat)
        
        # Count how many predictions fall within the tolerance
        accurate_count = np.sum(absolute_diff <= tolerancia)
        
        # Calculate the percentage of accurate predictions
        pia = accurate_count / len(y) * 100
                
        results.append(pia)
    
    return results


def calculate_accuracy(nota_original, nota_model):
    results = []
    for indice in range(0, 5):
        y = pegar_nota(nota_original, indice, True)
        y_hat = pegar_nota(nota_model, indice, True)
        
        # Calculate accuracy
        accuracy = accuracy_score(y, y_hat)
        
        results.append(accuracy)
        
    return results