from groq import Groq
import os
import google.generativeai as genai
import time
import ast
import re
import random

GEMINI_15_FLASH = "gemini-1.5-flash"
LLAMA_32_90B_TEXT_PREVIEW = "llama-3.2-90b-text-preview"

SLEEP_TIME = {}
SLEEP_TIME[GEMINI_15_FLASH] = 4
SLEEP_TIME[LLAMA_32_90B_TEXT_PREVIEW] = 2

def choose_model(model_cod = -1):

    if model_cod == -1:
        print("ATENTION - Choose the model:")
        print("1 - " + GEMINI_15_FLASH)
        print("2 - " + LLAMA_32_90B_TEXT_PREVIEW)
        print("3 - other")
        model_cod = int(input("Input the number you would like to execute: "))
    
    model_name = ""
    
    match model_cod:
        case 1:
            model_name = GEMINI_15_FLASH
        case 2:
            model_name = LLAMA_32_90B_TEXT_PREVIEW
        case _:
            print("Invalid model, choose another value:")
            model_name, model_cod = choose_model()
    
    print("Choosen Model: " + model_name)
    return model_name, model_cod

def model_setup(model_name, key_id):
    print(f"\n\n Setting model {model_name} with API Key {key_id} \n\n")
    if (key_id == -1) :
        key_id = random.randint(1, 5)
    
    if model_name == GEMINI_15_FLASH:
        GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY_' + str(key_id)]
        
        genai.configure(api_key=GOOGLE_API_KEY)
        
        model = genai.GenerativeModel(model_name=GEMINI_15_FLASH)
        print(model)
        chat = model.start_chat(enable_automatic_function_calling=True)
    elif model_name == LLAMA_32_90B_TEXT_PREVIEW:
        chat = Groq(api_key=os.environ.get("GROQ_API_KEY_" + str(key_id)))
    
    return chat

def run_model(essays_dataset, exp, ini, end, model_name, chat, dataset_name):
  essays_outputs = []

  for i in range(ini, end):
    if i == 34 and dataset_name == ("essaysGrade1000"):
      print("Skipping essay number: " + str(i))
      continue

    if (i == 101 or i == 131 or i == 143) and dataset_name == ("extended2024"):
      print("Skipping essay number: " + str(i))
      continue

    if (i == 97 or i == 98 or i == 112) and dataset_name == ("propor2024"):
      print("Skipping essay number: " + str(i))
      continue

    essay_data = essays_dataset[i]
    essay = essay_data["essay_text"]
    prompt = essay_data["id_prompt"].replace("-", " ")
    print("It will evaluated essay with number:" + str(i))
    prompt = exp.build_prompt(essay, prompt)
    grades, response = made_question(model_name, chat, prompt)

    print("Evaluated essay with number: " + str(i))

    model_key = model_name.split("-")[0]
    grades_key = model_key + "_grades"
    output_key = model_key + "_output"

    output = {
      "id": essay_data["id"],
      "essay_text": essay_data["essay_text"],
      "id_prompt": essay_data["id_prompt"],
      "grades": essay_data["grades"],
      grades_key: grades,
      output_key: response,
    }

    essays_outputs.append(output)

  return essays_outputs


def made_question(model_name, chat, prompt):
    prompt_divided = prompt.split("####")
    
    grades = ""
    reponse = ""
    sleep_time = SLEEP_TIME[model_name]
    pattern = r"(\d+)\D{0,3}(\d+)\D{0,3}(\d+)\D{0,3}(\d+)\D{0,3}(\d+)\D{0,3}(\d+)"

    try:
        for prompt in prompt_divided:
            time.sleep(sleep_time) # API Limit - no more that 60 requests per minute
            full_response, response = make_especific_model_question(model_name, chat, prompt)
        
        match = re.search(pattern, response)
        while not match:
            prompt = prompt_divided[-1]
            time.sleep(sleep_time) 
            print(response)
            full_response, response = make_especific_model_question(model_name, chat, prompt)
            match = re.search(pattern, response)
        
        grades = str(list(map(int, match.groups())))
    except Exception as e:
        print(f"There was an exception on made question: {e}")
        for prompt in prompt_divided:
            time.sleep(120)
            full_response, response = make_especific_model_question(model_name, chat, prompt)

        match = re.search(pattern, response)
        while not match:
            print(response)
            full_response, response = make_especific_model_question(model_name, chat, prompt)
            match = re.search(pattern, response)
        grades = str(list(map(int, match.groups())))
    
    return grades, full_response

def make_especific_model_question(model_name, chat, prompt):
    full_response = ""
    response = ""
    if model_name == GEMINI_15_FLASH:
        full_response = chat.send_message(prompt)
        response = full_response.text
    elif model_name == LLAMA_32_90B_TEXT_PREVIEW:
        completion = chat.chat.completions.create(
            model=LLAMA_32_90B_TEXT_PREVIEW,
            messages=[{
                "role": "user",
                "content": prompt
            }],
        )
        
        full_response_obj = completion.choices[0].message
        response = full_response_obj.content
        full_response = str(full_response_obj)

    return full_response, response