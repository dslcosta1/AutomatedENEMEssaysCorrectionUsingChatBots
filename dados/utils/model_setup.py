from groq import Groq
import os
import google.generativeai as genai
import time
import ast

GEMINI_15_FLASH = "gemini-1.5-flash"
LLAMA_32_90B_TEXT_PREVIEW = "llama-3.2-90b-text-preview"

SLEEP_TIME = {}
SLEEP_TIME[GEMINI_15_FLASH] = 4
SLEEP_TIME[LLAMA_32_90B_TEXT_PREVIEW] = 1

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

def model_setup(model_name):
    if model_name == GEMINI_15_FLASH:
        GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
        
        genai.configure(api_key=GOOGLE_API_KEY)
        
        model = genai.GenerativeModel(model_name=GEMINI_15_FLASH)
        print(model)
        chat = model.start_chat(enable_automatic_function_calling=True)
    elif model_name == LLAMA_32_90B_TEXT_PREVIEW:
        chat = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    return chat


def made_question(model_name, chat, prompt):
    prompt_divided = prompt.split("####")
    
    grades = ""
    reponse = ""
    sleep_time = SLEEP_TIME[model_name]

    for prompt in prompt_divided:
        time.sleep(4) # API Limit - no more that 60 requests per minute
        full_response, response = make_especific_model_question(model_name, chat, prompt)
        grades = ast.literal_eval(response.rstrip())
    """
    try:
        for prompt in prompt_divided:
            time.sleep(4) # API Limit - no more that 60 requests per minute
            response = make_especific_model_question(model_name, chat, prompt)
        grades = ast.literal_eval(response.text.rstrip())
    except:
        print("There was an exception on made question!!!")
        for prompt in prompt_divided:
            time.sleep(60)
            response = make_especific_model_question(model_name, chat, prompt)
        grades = ast.literal_eval(response.text.rstrip())
    """
    
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
        reponse = full_response_obj.content
        full_response = str(full_response_obj)

    return full_response, response