import re

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

def arrumar_nota(nota):
    possiveis_notas = [0, 40, 80, 120, 160, 200]
    mais_proxima = -1
    dif = 1000
    for n in possiveis_notas:
        if abs(nota - n) < dif:
            mais_proxima = n
            dif = abs(nota - n)
    return mais_proxima

def pegar_nota(lista_notas, indice, arrumar_nota=False):
    nova_nota = []
    for n in lista_notas:
        if arrumar_nota:
            nova_nota.append(arrumar_nota(n[indice]))
        else:
            nova_nota.append(n[indice])
    return nova_nota

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
        y = np.array(pegar_nota(nota_original, indice))
        y_hat = np.array(pegar_nota(nota_model, indice))
        
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
        y = np.array(pegar_nota(nota_original, indice))
        y_hat = np.array(pegar_nota(nota_model, indice))
        
        # Calculate the absolute differences
        absolute_diff = np.abs(y - y_hat)
        
        # Compute the mean of absolute differences
        mae = np.mean(absolute_diff)
        
        print(f"MAE: {mae}")
        
        results.append(mae)
    
    return results