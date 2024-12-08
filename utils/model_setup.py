from groq import Groq
from llamaapi import LlamaAPI
import os
import google.generativeai as genai
import time
import ast
import re
import random

GEMINI_15_FLASH = "gemini-1.5-flash"
LLAMA_32_90B_TEXT_PREVIEW = "llama-3.2-90b-text-preview"

SLEEP_TIME = {}
SLEEP_TIME[GEMINI_15_FLASH] = 0
SLEEP_TIME[LLAMA_32_90B_TEXT_PREVIEW] = 15

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
        google_api_id = 'GOOGLE_API_KEY'
        try:
            # Used to securely store your API key
            from google.colab import userdata
    
            # Or use `os.getenv('API_KEY')` to fetch an environment variable.
            GOOGLE_API_KEY=userdata.get(google_api_id)
        except Exception as e:
            import os
            GOOGLE_API_KEY = os.environ[google_api_id]
                
        genai.configure(api_key=GOOGLE_API_KEY)
        
        model = genai.GenerativeModel(model_name=GEMINI_15_FLASH)
        print(model)
        chat = model.start_chat(enable_automatic_function_calling=True)
    elif model_name == LLAMA_32_90B_TEXT_PREVIEW:
        
        groq_api_id = 'GROQ_API_KEY'
        try:
            # Used to securely store your API key
            from google.colab import userdata
    
            # Or use `os.getenv('API_KEY')` to fetch an environment variable.
            GROQ_API_KEY=userdata.get(groq_api_id)
        except Exception as e:
            import os
            GROQ_API_KEY = os.environ[groq_api_id]
        
        chat = Groq(api_key=GROQ_API_KEY)
        """

        llama_api_id = 'LLAMA_API_KEY'
        try:
            # Used to securely store your API key
            from google.colab import userdata
    
            # Or use `os.getenv('API_KEY')` to fetch an environment variable.
            LLAMA_API_KEY=userdata.get(llama_api_id)
        except Exception as e:
            import os
            LLAMA_API_KEY = os.environ[llama_api_id]
        
        chat = LlamaAPI(LLAMA_API_KEY)      
        """
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
    supporting_text = essay_data["supporting_text"]
    print("It will evaluated essay with number:" + str(i))
    prompt = exp.build_prompt(essay, prompt, supporting_text)
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
    #pattern = r"(\d+)\D{0,3}(\d+)\D{0,3}(\d+)\D{0,3}(\d+)\D{0,3}(\d+)\D{0,3}(\d+)"
    pattern = r"(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)\D+(\d+)"
    prompt_history = ""
    
    try:
        for prompt in prompt_divided:
            prompt_history += prompt
            time.sleep(sleep_time) # API Limit - no more that 60 requests per minute
            full_response, response = make_especific_model_question(model_name, chat, prompt_history)
            prompt_history += "\n\n" + response + "\n\n"
        
        match = re.search(pattern, response)
        while not match:
            print(f"There was not a match!!")
            prompt = prompt_history
            time.sleep(sleep_time) 
            print(response)
            full_response, response = make_especific_model_question(model_name, chat, prompt_history)
            match = re.search(pattern, response)
        
        grades = str(list(map(int, match.groups())))
    except Exception as e:
        print(f"There was an exception on made question: {e}")
        prompt_history = ""
        for prompt in prompt_divided:
            time.sleep(10)
            prompt_history += prompt
            full_response, response = make_especific_model_question(model_name, chat, prompt_history)
            prompt_history += "\n\n" + response + "\n\n"

        match = re.search(pattern, response)
        while not match:
            print(response)
            full_response, response = make_especific_model_question(model_name, chat, prompt_history)
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
            model="llama-3.1-70b-versatile",
            messages=[{
                "role": "user",
                "content": prompt
            }],
        )
        
        full_response_obj = completion.choices[0].message
        response = full_response_obj.content
        full_response = str(full_response_obj)
        """
        # Build the API request
        api_request_json = {
            "model": "llama3.1-70b",
            "messages": [
                {"role": "user", 
                 "content": prompt},
            ],
        }
        
        # Execute the Request
        full_response = chat.run(api_request_json)
        response = full_response.json()['choices'][0]['message']['content']
        """
    return full_response, response