import tkinter as tk
from tkinter import ttk
import sys
import time
from datetime import datetime, timedelta, timezone
import os
import platform
import subprocess
import stat
from threading import Thread
from ttkthemes import ThemedTk
from langdetect import detect
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import openai
import re
from helper_functions import detect_phone_number, contains_emoji, emoji_reducer, should_ask_question, find_and_replace_questions, count_A_lines, remove_question
import requests
import json
from tkinter import messagebox
import firebase_admin
from firebase_admin import auth
import threading
import time 
from dotenv import load_dotenv
import re
load_dotenv()



emoji_mapping = {
    "(wink emoji)": "😉",
    "(smile emoji)": "😄",
    "(sad emoji)": "😢",
    "(heart emoji)": "❤️",
    "(thumbs up emoji)": "😃",
    "(smirk emoji)": "😏"  # Added smirk emoji
    # Add more as needed
}

def complex_method(formatted_text2, name, language):
    # Get last line of the chat so we know what language we're speaking in 
    # Split the text into lines
    lines = formatted_text2.strip().split('\n')

    # Initialize an empty string to hold lines that start with "G:"
    g_lines = ""

    # Iterate through each line
    for line in lines:
        if line.startswith("G:"):
            # Remove the "G:" and append the line to g_lines
            g_lines += line[2:].strip() + " "

    # Remove the trailing space
    g_lines = g_lines.rstrip()



    if detect(g_lines) == 'es' or detect(g_lines) == 'nl' or detect(g_lines) == 'sl' or detect(g_lines) == 'ca' or detect(g_lines) == 'sl' :
        print("detected lang is: ", detect(g_lines))
        language = "Spanish"
        print("Spanish detected. Conv will be in Spanish")
    else:
        print("detected lang is: ", detect(g_lines))
        language = "English"
        print("English detected. Conv will be in English")

    # if detect_phone_number(formatted_text2, name):
    #     print("Exiting due to phone number.")
    #     #exit() # this one works in a normal python script.
    #     sys.exit(0)  # Use sys.exit() to terminate the entire script





    print("Conv will be in: ", language)

    # Define parameterized variables at the top for easy modification
    if language != 'Spanish':
        OPENER_FILE = "01-processing-files/01-split-sys-msg-method/01-opener-sys-msg.txt"
        GETTING_TO_KNOW_FILE = "01-processing-files/01-split-sys-msg-method/02-getting2know-sys-msg.txt"
        SOFT_CLOSE_MID_FILE = "01-processing-files/01-split-sys-msg-method/03-soft-close-mid-sys-msg.txt"
        HARD_CLOSE_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg.txt"
    else:
        OPENER_FILE = "01-processing-files/01-split-sys-msg-method/01-opener-sys-msg-es.txt"
        GETTING_TO_KNOW_FILE = "01-processing-files/01-split-sys-msg-method/02-getting2know-sys-msg-es.txt"
        SOFT_CLOSE_MID_FILE = "01-processing-files/01-split-sys-msg-method/03-soft-close-mid-sys-msg-es.txt"
        HARD_CLOSE_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg-es.txt"















    # Configure OpenAI API client
    with open("00-credentials/00-openai-key.txt", "r") as f:
        api_key = f.read().strip()

    openai.api_key = api_key

    # Determine which system message file to read based on conditions
    num_A_lines = count_A_lines(formatted_text2)

    day_of_week = datetime.now().strftime('%A')

    english_question_list = [
        "Where are you from originally?", 
        "daily question"
    ]

    spanish_question_list = [
        "de donde eres originalmente?",
        "pregunta del dia"
    ]

    spanish_daily_question_list = [
        "Cómo te trata el Lunes de Lujo?",
        "Cómo va tu Martes Maravilloso?",
        "Cómo te va en el Miércoles Melódico?",
        "Cómo va tu Jueves Jugoso?",
        "Cómo va tu Viernes de Vino?",
        "Qué tal el Sábado de Sofá?",
        "Cómo te trata el Domingo Dulce?"
    ]


    english_daily_question_list = [
        "How goes your funday sunday?",
        "How goes your taco tuesday?",
        "How's your Mocha Monday treating you?",
        "How's your wonderful wednesday?",
        "How's your thirsty Thursday treating you?",
        "How's your Fabulous Friday going?",
        "How goes your soulful Saturday?",
        "How's your sunday funday?"
    ]


    weekday_translation = {
        "monday": "lunes",
        "tuesday": "martes",
        "wednesday": "miércoles",
        "thursday": "jueves",
        "friday": "viernes",
        "saturday": "sábado",
        "sunday": "domingo"
    }


    today = datetime.now().strftime('%A').lower()
    if language == 'Spanish':
        today = weekday_translation.get(today, today)

    print("Number of A lines:", num_A_lines)
    if num_A_lines <= 1:
        system_message_file = OPENER_FILE

    elif 2 <= num_A_lines <= 3:
        system_message_file = GETTING_TO_KNOW_FILE
        #assistant_reply = find_and_replace_questions(assistant_reply, day_of_week, english_question_list, spanish_question_list)

    else:
        # Run a completion to determine "Yes" or "No"
        with open("01-processing-files/01-split-sys-msg-method/03a-soft-close-detector-mid-sys-msg.txt", "r") as f:
            temp_system_message = f.read().strip()

        content = '{prompt}: \n "{text}"'.format(prompt=temp_system_message, text=formatted_text2)
        messages = [{"role": "user", "content": content}]
        response = get_response(messages, "admin")
        assistant_reply = response['choices'][0]['message']['content']

        print("Soft close detector says: ", assistant_reply)
        soft_close_reason = assistant_reply
        match = re.search(r"Decision: (Yes|No)", assistant_reply)
        if match:
            decision = match.group(1)
        print(decision)
        if decision == "No":
            print("No soft close detected yet")
            system_message_file = SOFT_CLOSE_MID_FILE
        else:
            print("Soft close detected - now ask for number")
            system_message_file = HARD_CLOSE_FILE

    # Read the selected system message
    with open(system_message_file, "r") as f:
        system_message = f.read().strip()
        
    # Get the current day
    current_day = datetime.now().strftime('%A')  # This will give you the day like 'Monday', 'Tuesday', etc.

    # Replace "[today]" with the current day in the system_message
    if "Today is [today]" in system_message:
        system_message = system_message.replace("[today]", current_day)
    if "[gname]" in system_message:
        system_message = system_message.replace("[gname]", name)
        
    

    # Define the messages list with the {text} field
    content = '{prompt}: \n "{text}"'.format(prompt=system_message, text=formatted_text2)
    messages = [{"role": "user", "content": content}]

    # Use openai.ChatCompletion.create() with the updated messages list
    while True:
        # Use openai.ChatCompletion.create() with the updated messages list
        response = get_response(messages, "admin")
        

        assistant_reply = response['choices'][0]['message']['content']
        print("Assistant reply RAW: ", assistant_reply)
        # Break out of the loop if assistant_reply doesn't contain a question mark,
        # or if we are not using the OPENER_FILE.
        if "?" not in assistant_reply or system_message_file != OPENER_FILE:
            print("Reply doesnt contain a question or we're not in the opening stage, so take reply")
            break
        print("You're in the opening stage and assistant has given a question. Roll again.")

    assistant_reply = emoji_reducer(formatted_text2, assistant_reply)       
    assistant_reply = assistant_reply.replace("!", "")
    assistant_reply = assistant_reply.replace("¡", "")
    assistant_reply = assistant_reply.replace("A:", "")
    assistant_reply = assistant_reply.replace("¿", "")
    assistant_reply = assistant_reply.replace("?", "")
    #assistant_reply = assistant_reply.encode('latin1').decode('utf-8')
    assistant_reply = assistant_reply.lower()
    assistant_reply = assistant_reply.replace("\"", "")
    assistant_reply = assistant_reply.split('\n')[0]

    if system_message_file == OPENER_FILE:


        # Randomly choose a question based on the language
        question = random.choice(english_question_list if language == 'English' else spanish_question_list)

        # If the question is a "daily question", then choose an appropriate daily question
        if question == "daily question":
            question = next((q for q in english_daily_question_list if today in q.lower()), "How's your day?")
        elif question == "pregunta del dia":
            question = next((q for q in spanish_daily_question_list if today in q.lower()), "Cómo te va el día?")

        # Convert to lowercase and remove the '?'
        question = question.lower().replace('?', '')

        # Add the question to the assistant's reply
        if not assistant_reply.endswith('.'):
            assistant_reply += '.'

        assistant_reply += " " + question




    # Modify assistant reply based on conditions
    # if system_message_file == GETTING_TO_KNOW_FILE:
    #     if should_ask_question(formatted_text2):
    #         print("Original ass reply; ", assistant_reply)
    #         assistant_reply = find_and_replace_questions(assistant_reply, day_of_week, english_question_list, spanish_question_list, language)




    # if system_message_file == GETTING_TO_KNOW_FILE:
    #     print(assistant_reply)
    #     assistant_reply = remove_question(assistant_reply)
    #     print("Removed question")


    # Call emoji_reducer function to modify assistant_reply
    assistant_reply = fix_text(assistant_reply)
    try:
        assistant_reply = assistant_reply.encode('latin1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError) as e:
        print("Error:", e)
        print("Original text:", assistant_reply)


    for text, emoji in emoji_mapping.items():
        assistant_reply = assistant_reply.replace(text, emoji)

    # Splitting the text into lines
    lines = assistant_reply.split('\n')

    # Taking the first line
    assistant_reply2 = lines[0]

    print("File used:", system_message_file)
    print("Assistant reply:", assistant_reply2)
    return assistant_reply2

def simple_method(formatted_text2, name, language):

    # Get last line of the chat so we know what language we're speaking in 
    # Split the text into lines
    lines = formatted_text2.strip().split('\n')


    # Initialize an empty string to hold lines that start with "G:"
    g_lines = ""

    # Iterate through each line
    for line in lines:
        if line.startswith("G:"):
            # Remove the "G:" and append the line to g_lines
            g_lines += line[2:].strip() + " "

    # Remove the trailing space
    g_lines = g_lines.rstrip()



    if detect(g_lines) == 'es' or detect(g_lines) == 'nl' or detect(g_lines) == 'nl' or detect(g_lines) == 'ca' :
        print("detected lang is: ", detect(g_lines))
        language = "Spanish"
        print("Spanish detected. Conv will be in Spanish")
    else:
        print("detected lang is: ", detect(g_lines))
        language = "English"
        print("English detected. Conv will be in English")

    # if detect_phone_number(formatted_text2, name):
    #     print("Exiting due to phone number.")
    #     #exit() # this one works in a normal python script.
    #     sys.exit(0)  # Use sys.exit() to terminate the entire script




    print("Language used is: ", language)



    # Define parameterized variables at the top for easy modification
    if language != 'Spanish':
        OPENER_FILE = "01-processing-files/02-simple-method/01-opener-sys-msg.txt"
        second_message = "01-processing-files/02-simple-method/02-que-haces-pa-divertirte-response.txt"
        third_message = "01-processing-files/02-simple-method/03-de-donde-eres.txt"
        GETTING_TO_KNOW_FILE = "01-processing-files/01-split-sys-msg-method/02-getting2know-sys-msg.txt"
        SOFT_CLOSE_MID_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg.txt"
        HARD_CLOSE_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg.txt"
    else:
        OPENER_FILE = "01-processing-files/02-simple-method/01-opener-sys-msg-es.txt"
        second_message = "01-processing-files/02-simple-method/02-que-haces-pa-divertirte-response-es.txt"
        third_message = "01-processing-files/02-simple-method/03-de-donde-eres-es.txt"
        GETTING_TO_KNOW_FILE = "01-processing-files/01-split-sys-msg-method/02-getting2know-sys-msg-es.txt"
        SOFT_CLOSE_MID_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg-es.txt"
        HARD_CLOSE_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg-es.txt"













    # Configure OpenAI API client
    with open("00-credentials/00-openai-key.txt", "r") as f:
        api_key = f.read().strip()

    openai.api_key = api_key

    # Determine which system message file to read based on conditions
    num_A_lines = count_A_lines(formatted_text2)

    day_of_week = datetime.now().strftime('%A')

    english_question_list = [
        "What do you do for fun?" ]

    spanish_question_list = [
        "¿Qué haces para divertirte?"

    ]

    spanish_daily_question_list = [
        "Cómo te trata el Lunes de Lujo?",
        "Cómo va tu Martes Maravilloso?",
        "Cómo te va en el Miércoles Melódico?",
        "Cómo va tu Jueves Jugoso?",
        "Cómo va tu Viernes de Vino?",
        "Qué tal el Sábado de Sofá?",
        "Cómo te trata el Domingo Dulce?"
    ]


    english_daily_question_list = [
        "How goes your funday sunday?",
        "How goes your taco tuesday?",
        "How's your Mocha Monday treating you?",
        "How's your wonderful wednesday?",
        "How's your thirsty Thursday treating you?",
        "How's your Fabulous Friday going?",
        "How goes your soulful Saturday?",
        "How's your sunday funday?"
    ]


    weekday_translation = {
        "monday": "lunes",
        "tuesday": "martes",
        "wednesday": "miércoles",
        "thursday": "jueves",
        "friday": "viernes",
        "saturday": "sábado",
        "sunday": "domingo"
    }


    today = datetime.now().strftime('%A').lower()
    current_day = datetime.now().strftime('%A')
    if language == 'Spanish':
        today = weekday_translation.get(today, today)

    print("Number of A lines:", num_A_lines)
    if num_A_lines <= 1:
        system_message_file = OPENER_FILE

    elif 2 <= num_A_lines <= 2:
        system_message_file = second_message
        #assistant_reply = find_and_replace_questions(assistant_reply, day_of_week, english_question_list, spanish_question_list)


    elif 3 <= num_A_lines <= 3:
        system_message_file = third_message
        #assistant_reply = find_and_replace_questions(assistant_reply, day_of_week, english_question_list, spanish_question_list)
    elif 4 <= num_A_lines <= 5:
        system_message_file = GETTING_TO_KNOW_FILE

    else:
        # Run a completion to determine "Yes" or "No"
        with open("01-processing-files/01-split-sys-msg-method/03a-soft-close-detector-mid-sys-msg.txt", "r") as f:
            temp_system_message = f.read().strip()
        if "Today is [today]" in system_message:
            temp_system_message = temp_system_message.replace("[today]", current_day)
        content = '{prompt}: \n "{text}"'.format(prompt=temp_system_message, text=formatted_text2)
        messages = [{"role": "user", "content": content}]
        response = get_response(messages, "admin")

        assistant_reply = response['choices'][0]['message']['content']

        print("Soft close detector says: ", assistant_reply)
        soft_close_reason = assistant_reply
        match = re.search(r"Decision: (Yes|No)", assistant_reply)
        if match:
            decision = match.group(1)
        print(decision)
        if decision == "No":
            print("No soft close detected yet")
            system_message_file = SOFT_CLOSE_MID_FILE
        else:
            print("Soft close detected - now ask for number")
            system_message_file = HARD_CLOSE_FILE

    # Read the selected system message
    with open(system_message_file, "r") as f:
        system_message = f.read().strip()
    if "Today is [today]" in system_message:
        system_message = system_message.replace("[today]", current_day)
    if "[gname]" in system_message:
        system_message = system_message.replace("[gname]", name)
    # Define the messages list with the {text} field
    content = '{prompt}: \n "{text}"'.format(prompt=system_message, text=formatted_text2)
    messages = [{"role": "user", "content": content}]

    # Use openai.ChatCompletion.create() with the updated messages list
    while True:
        # Use openai.ChatCompletion.create() with the updated messages list
        response = get_response(messages, "admin")


        assistant_reply = response['choices'][0]['message']['content']
        print("Assistant reply RAW: ", assistant_reply)
        # Break out of the loop if assistant_reply doesn't contain a question mark,
        # or if we are not using the OPENER_FILE.
        if "?" not in assistant_reply or system_message_file == GETTING_TO_KNOW_FILE or system_message_file==SOFT_CLOSE_MID_FILE or system_message_file==HARD_CLOSE_FILE:# or system_message != OPENER_FILE or system_message!=second_message or system_message!=third_message:
            print("Reply doesnt contain a question or we're not in the opening stage, so take reply")
            break
        print("You're in the opening stage and assistant has given a question. Roll again.")
        time.sleep(5)
        

    # Call emoji_reducer function to modify assistant_reply
    assistant_reply = emoji_reducer(formatted_text2, assistant_reply)       
    assistant_reply = assistant_reply.replace("!", "")
    assistant_reply = assistant_reply.replace("¡", "")
    assistant_reply = assistant_reply.replace("A:", "")
    assistant_reply = assistant_reply.replace("¿", "")
    assistant_reply = assistant_reply.replace("?", "")
    #assistant_reply = assistant_reply.encode('latin1').decode('utf-8')
    assistant_reply = assistant_reply.lower()
    assistant_reply = assistant_reply.replace("\"", "")
    assistant_reply = assistant_reply.split('\n')[0]
        
        

    print("reply before doing full stop and addition:" ,assistant_reply)
    if system_message_file == OPENER_FILE:


        # Randomly choose a question based on the language
        question = random.choice(english_question_list if language == 'English' else spanish_question_list)

        # If the question is a "daily question", then choose an appropriate daily question
        if question == "daily question":
            question = next((q for q in english_daily_question_list if today in q.lower()), "How's your day?")
        elif question == "pregunta del dia":
            question = next((q for q in spanish_daily_question_list if today in q.lower()), "Cómo te va el día?")

        # Convert to lowercase and remove the '?'
        #question = question.lower().replace('?', '')

        # Add the question to the assistant's reply
        if not assistant_reply.endswith('.'):
            assistant_reply += '.'

        assistant_reply += " " + question

    if system_message_file == second_message:
        print("reply second msg" ,assistant_reply)
        if not assistant_reply.endswith('.'):
            assistant_reply += '.'

        # Read the content from the file
        with open('01-processing-files/02-simple-method/02a-question-tag-es.txt', 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Append the content to assistant_reply
        assistant_reply += " " + file_content    

    if system_message_file == third_message:
        print("reply third msg" ,assistant_reply)
        if not assistant_reply.strip().endswith('.') and not assistant_reply.strip().endswith('?'):
            assistant_reply = assistant_reply.strip() + '.'

        # Read the content from the file
        with open('01-processing-files/02-simple-method/03a-question-tag-es.txt', 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Append the content to assistant_reply
        assistant_reply += " " + file_content    


    # Modify assistant reply based on conditions
    # if system_message_file == GETTING_TO_KNOW_FILE:
    #     if should_ask_question(formatted_text2):
    #         print("Original ass reply; ", assistant_reply)
    #         assistant_reply = find_and_replace_questions(assistant_reply, day_of_week, english_question_list, spanish_question_list, language)



    # if system_message_file == GETTING_TO_KNOW_FILE:
    #     print(assistant_reply)
    #     assistant_reply = remove_question(assistant_reply)
    #     print("Removed question")


    assistant_reply = fix_text(assistant_reply)
    try:
        assistant_reply = assistant_reply.encode('latin1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError) as e:
        print("Error:", e)
        print("Original text:", assistant_reply)


    for text, emoji in emoji_mapping.items():
        assistant_reply = assistant_reply.replace(text, emoji)

    # Splitting the text into lines
    lines = assistant_reply.split('\n')

    # Taking the first line
    assistant_reply2 = lines[0]

    print("File used:", system_message_file)
    print("Assistant reply:", assistant_reply2)
    return assistant_reply2

# chromedriver_path = r'04-assets\\chromedriver.exe'
# extension_path2 = r'04-assets\\uBlock-Origin.crx'
# chrome_options = webdriver.ChromeOptions()
# #chrome_options.add_extension(extension_path2)
# chrome_options.add_argument('--start-maximized') 



class RedirectStdout:
    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)

    def flush(self):
        pass  # Add a flush method to avoid the error












def execute_first_messages():


    language = language_combo.get()
    simple_mode = simple_mode_var.get() 
    try:
        #print("Executing first messages...")
        chromedriver_path = r'04-assets\\chromedriver.exe'
        extension_path2 = r'04-assets\\uBlock-Origin.crx'
        #chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_extension(extension_path2)
        #chrome_options.add_argument('--start-maximized') 
                

        # Your profile folder name
        profile_folder_name = 'Autoflirt_profiles'

        # Get the user's home directory
        home_directory = os.path.expanduser("~")

        # Your profile directory path
        profile_directory = os.path.join(home_directory, profile_folder_name)

        # Create the directory if it doesn't exist
        if not os.path.exists(profile_directory):
            os.makedirs(profile_directory)
            # Change permissions
            if platform.system() == 'Windows':
                subprocess.run(['attrib', '-R', profile_directory])
            else:
                os.chmod(profile_directory, stat.S_IRWXU)
            first_time = True
        else:
            first_time = False
            
        ## Change profile folder to not read only 
        if platform.system() == 'Windows':
            subprocess.run(['attrib', '-R', profile_directory])
        else:
            os.chmod(profile_directory, stat.S_IRWXU)   
            

        # Check if the directory is empty
        is_empty = not bool(os.listdir(profile_directory))

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=1920x1080")
        #chrome_options.add_argument("--start-minimized")
        chrome_options.add_argument(f"user-data-dir={profile_directory}")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--disable-logging")
        #chrome_options.add_argument('--headless')  # Enables headless mode
        

        try:
            driver.quit()
        except:
            pass
        
        
        
         ########################## 0. Define the driver (somtimes errors)

        for attempt in range(1, 4):
            try:
                # service = webdriver.chrome.service.Service(executable_path=chromedriver_path)
                # service.start()
                driver_path = ChromeDriverManager().install()
                print(f"Driver path: {driver_path}")
                print(f"Driver path type: {type(driver_path)}")
                driver = webdriver.Chrome(driver_path, options=chrome_options)
                print(f"Successfully initialized WebDriver")
                print(f"Successfully initialized WebDriver on attempt {attempt}")
                time.sleep(random.uniform(3, 6))
                break  # Exit the loop if initialization is successful
            except Exception as e:
                print(f"Failed to initialize WebDriver on attempt {attempt}: {e}")
                print(f"Failed to initialize WebDriver: {e}")
                import traceback
                traceback.print_exc()
                try:
                    driver.quit()
                except:
                    pass  # Do nothing if driver.quit() fails
                if attempt == 3:
                    print("Reached maximum number of attempts. Exiting.")
                    exit(1)
                    
        ######################### END 0. Define the driver       
        driver.minimize_window()
        # service = webdriver.chrome.service.Service(executable_path=chromedriver_path)
        # service.start()
        # driver = webdriver.Chrome(options=chrome_options)
        time.sleep(random.uniform(3, 6))
        # Open the website
        driver.get('https://www.tinder.com/')
        driver.execute_script('document.title = "AutoConvos"')
        

        # If it's the first time or the directory was empty, ask the user to log in manually
            

        #time.sleep(60)  # 60 seconds, change it to the time you need

        print("Waiting for 'Matches' button to appear.")
        if manual_login_var.get() == 1 :
            print("First time user detected - you must log in.")
            print("After first time log in you need not log in again.")
            wait = WebDriverWait(driver, 120)
            matches_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Matches']")))
        else:
            wait = WebDriverWait(driver, 20)
            matches_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Matches']")))
        

        # Optional: Wait for any obstructing elements to disappear
        # Replace 'obstructing_element_selector' with the actual selector
        # wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, "obstructing_element_selector")))


        try:
            # Try to find the "Allow" button and click it if it exists
            wait = WebDriverWait(driver, 3)  # Wait for up to 3 seconds
            allow_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Maybe later']")))
            print("Maybe laber clicked")
            allow_button.click()
        except TimeoutException:
            # If the "Allow" button doesn't appear in 3 seconds, continue with the rest of the code
            print("Maybe later button not found. Continuing...")




        ###############################  START 1. Click matches
        try:
            time.sleep(random.uniform(2, 4))
            print("Clicking the 'Matches' button.")
            matches_button.click()
            print("'Matches' button clicked.")
        except Exception as e:
            print("Failed to click 'Matches' button. Trying JavaScript click.")
            driver.execute_script("arguments[0].click();", matches_button)
            print("'Matches' button clicked using JavaScript.")
            
        try:
            time.sleep(random.uniform(2, 4))
            print("Clicking the 'Matches' button.")
            matches_button.click()
            print("'Matches' button clicked.")
        except Exception as e:
            print("Failed to click 'Matches' button. Trying JavaScript click.")
            driver.execute_script("arguments[0].click();", matches_button)
            print("'Matches' button clicked using JavaScript.")    
        # Now to click the third li in the first ul


        ###############################  END 1. Click matches
            

            
        ############################### START 1a. Get the amount of matches  
            
        # Find all 'li' elements on the page with the specific style
        li_elements_with_style = driver.find_elements(By.XPATH, "//li[@style='width: 33.33%;']")

        # Get the count of such 'li' elements
        count_of_li_with_style = len(li_elements_with_style)

        # Print the count
        print(f"Number of li elements with style='width: 33.33%;': {count_of_li_with_style}")




        ############################### END 1a. Get the amount of matches 



        ############################### START 1b. Determine if user has gold or not


        try:
            element = driver.find_element(By.XPATH, "//*[contains(@class, 'ds-background-gold')]")
            first_match = 3
        except NoSuchElementException:
            first_match = 2



        ############################### END 1b. Determine if user has gold or not






        for i in range(count_of_li_with_style):
            if not should_run['first_messages']:
                print("Stopping First Messaging execution...")
                break  # This will exit the loop and stop the execution
            print(f"Loop iteration {i+1}")
            
            # ###############################  START 2. Click First Match

            # print(f"Locating the {i} 'li'.")
            # first_li = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[@style='width: 33.33%;'][1]")))
            # print("is the element displayed?", li_elements_with_style[first_match].is_displayed())
            # print("is the element enabled?", li_elements_with_style[first_match].is_enabled())
            # #third_li = driver.find_element(By.XPATH, f"//li[@style='width: 33.33%;'][{first_match}]")
            # third_li = li_elements_with_style[first_match]
            # driver.execute_script("arguments[0].scrollIntoView();", third_li)
            # #time.sleep(1000)
            # try:
            #     print(f"Clicking the {i} 'li'.")
            #     third_li.click()
            #     print(f"{i} 'li' clicked.")
            # except Exception as e:
            #     print(f"Failed to click {i} 'li': {e}. Trying JavaScript click.")
            #     driver.execute_script("arguments[0].click();", third_li)
            #     print(f"{i} 'li' clicked using JavaScript.")




            # ###############################  END 2. Click First Match 



            ###############################  START 2. Click First Match

            print("Locating the third 'li' in the first 'ul'.")
            third_li = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//ul)[1]/li[{first_match}]")))

            try:
                print("Clicking the third 'li'.")
                third_li.click()
                time.sleep(random.uniform(3, 6))
                print("Third 'li' clicked.")
            except Exception as e:
                print(f"Failed to click third 'li': {e}. Trying JavaScript click.")
                driver.execute_script("arguments[0].click();", third_li)
                print("Third 'li' clicked using JavaScript.")
                
            






            ###############################  END 2. Click First Match 




            ################################ START  3. Cold Opener Text and Send

            # Assuming 'driver' is your WebDriver instance
            time.sleep(random.uniform(3, 6))
            # Read the file into a list
            if language == 'Spanish':
                if simple_mode == 0:
                    with open('messages/01-cold-openers-es.txt', 'r') as file:
                        lines = file.readlines()
                    lines = [line for line in lines if line.strip()]
                else:
                    with open('messages/02-cold-opener-simple-method-es.txt', 'r') as file:
                        lines = file.readlines()
                    lines = [line for line in lines if line.strip()] 
                    
            else:
                if simple_mode == 0: 
                    with open('messages/01-cold-openers.txt', 'r') as file:
                        lines = file.readlines()
                    lines = [line for line in lines if line.strip()]
                else:
                    with open('messages/02-cold-opener-simple-method.txt', 'r') as file:
                        lines = file.readlines()
                    lines = [line for line in lines if line.strip()]
                
                

            # Remove any leading/trailing whitespace from each line
            lines = [line.strip() for line in lines]

            # Randomly pick a line from the list
            random_line = random.choice(lines)
            print("Line to send: ", random_line)
            try:
                random_line = random_line.encode('latin1').decode('utf-8')
            except (UnicodeDecodeError, UnicodeEncodeError) as e:
                print("Error:", e)
                print("Original text:", random_line)
            print("Line to send after clear: ", random_line)

            # Assuming 'driver' is your initialized WebDriver instance
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()

            actions.send_keys(random_line).perform()
            print(f"Send message {random_line}")
            time.sleep(random.uniform(4, 8))
            actions.send_keys(Keys.RETURN)  # Sending the Enter key
            time.sleep(random.uniform(4, 8))
            if toggle_var.get() == 1:
                actions.perform()  # Perform the action
            else: 
                print("Active Mode OFF - Message will not be sent")
            print(f"Pressed Enter")


            ############################### END 3. Cold Opener Text and Send 





            ################################ START  4. Need to go back to matches to send more colds

            try:
                time.sleep(random.uniform(3, 6))
                print("Clicking the 'Matches' button.")
                matches_button.click()
                print("'Matches' button clicked.")
            except Exception as e:
                print("Failed to click 'Matches' button. Trying JavaScript click.")
                driver.execute_script("arguments[0].click();", matches_button)
                print("'Matches' button clicked using JavaScript.")

            try:
                time.sleep(random.uniform(2, 4))
                print("Clicking the 'Matches' button.")
                matches_button.click()
                print("'Matches' button clicked.")
            except Exception as e:
                print("Failed to click 'Matches' button. Trying JavaScript click.")
                driver.execute_script("arguments[0].click();", matches_button)
                print("'Matches' button clicked using JavaScript.")    
            # Now to click the third li in the first ul
            #first_match+=1  


            ############################### END  4. Need to go back to matches to send more colds



        #how many lis are there - that's the length of the loop. 

        # Close the driver but don't delete the profile
        print("That's all the messages done for now")
        driver.quit()

        print("First messages execution complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
    time.sleep(1)

def execute_conversations():

    global days_entry, language_combo
    days_threshold = int(days_entry.get())
    convs_amt = int(conversations_entry.get())
    language = language_combo.get()
    try:
        #print("Executing conversations...")
        
    

        # Your profile folder name
        profile_folder_name = 'Autoflirt_profiles'

        # Get the user's home directory
        home_directory = os.path.expanduser("~")

        # Your profile directory path
        profile_directory = os.path.join(home_directory, profile_folder_name)

        # Create the directory if it doesn't exist
        if not os.path.exists(profile_directory):
            os.makedirs(profile_directory)
            # Change permissions
            if platform.system() == 'Windows':
                subprocess.run(['attrib', '-R', profile_directory])
            else:
                os.chmod(profile_directory, stat.S_IRWXU)
            first_time = True
        else:
            first_time = False
            
        ## Change profile folder to not read only 
        if platform.system() == 'Windows':
            subprocess.run(['attrib', '-R', profile_directory])
        else:
            os.chmod(profile_directory, stat.S_IRWXU)   
            

        # Check if the directory is empty
        is_empty = not bool(os.listdir(profile_directory))

        #chrome_options = webdriver.ChromeOptions()
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_extension(extension_path2)
        chrome_options.add_argument("--window-size=1920x1080")
        #chrome_options.add_argument("--start-minimized")
        chrome_options.add_argument(f"user-data-dir={profile_directory}")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--disable-logging")
        #chrome_options.add_argument('--headless')  # Enables headless mode

        try:
            driver.quit()
        except:
            pass



        ########################## 0. Define the driver (somtimes errors)

        for attempt in range(1, 4):
            try:
                # service = webdriver.chrome.service.Service(executable_path=chromedriver_path)
                # service.start()
                driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
                print(f"Successfully initialized WebDriver on attempt {attempt}")
                time.sleep(random.uniform(3, 6))
                break  # Exit the loop if initialization is successful
            except Exception as e:
                print(f"Failed to initialize WebDriver on attempt {attempt}: {e}")
                try:
                    driver.quit()
                except:
                    pass  # Do nothing if driver.quit() fails
                if attempt == 3:
                    print("Reached maximum number of attempts. Exiting.")
                    exit(1)
                    
        ######################### END 0. Define the driver             
                    
                    
                    
                    
        driver.minimize_window()       
        driver.get('https://www.tinder.com/')   
        
        # Open the website
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                time.sleep(5)
                driver.get('https://www.tinder.com/')
                print(f"Successfully navigated to Tinder.com on attempt {attempt}")
                break  # Break the loop if the site is successfully loaded
            except WebDriverException as e:
                print(f"Failed to navigate to Tinder.com on attempt {attempt}: {e}")
                if attempt < max_attempts:
                    print("Retrying...")
                    time.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    print("Max attempts reached. Exiting.")
            # You may choose to close the driver or handle the exception in another way

        # If it's the first time or the directory was empty, ask the user to log in manually

        #time.sleep(60)  # 60 seconds, change it to the time you need
        
        driver.execute_script('document.title = "AutoConvos"') 
        print("Waiting for 'Messages' button to appear.")
        if manual_login_var.get() == 1 :
            print("First time user detected - you must log in.")
            print("After first time log in you need not log in again.")
            wait = WebDriverWait(driver, 120)
            messages_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Messages']")))
        else:
            wait = WebDriverWait(driver, 20)
            messages_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Messages']")))


        try:
            # Try to find the "Allow" button and click it if it exists
            wait = WebDriverWait(driver, 10)  # Wait for up to 3 seconds
            allow_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Maybe later']")))
            print("Maybe laber clicked")
            allow_button.click()
        except TimeoutException:
            # If the "Allow" button doesn't appear in 3 seconds, continue with the rest of the code
            print("Maybe later button not found. Continuing...")

        ###############################  START 1. Click Messages
        try:
            time.sleep(random.uniform(2, 4))
            print("Clicking the 'Messages' button.")
            messages_button.click()
            print("'Messages' button clicked.")
        except Exception as e:
            print("Failed to click 'Messages' button. Trying JavaScript click.")
            driver.execute_script("arguments[0].click();", messages_button)
            print("'Messages' button clicked using JavaScript.")
            
        try:
            time.sleep(random.uniform(2, 4))
            print("Clicking the 'Messages' button.")
            driver.execute_script("arguments[0].click();", messages_button)
            
            print("'Messages' button clicked.")
        except Exception as e:
            print("Failed to click 'Messages' button. Trying JavaScript click.")
            messages_button.click()
            print("'Messages' button clicked using JavaScript.")    

        try:
            time.sleep(random.uniform(2, 4))
            print("Clicking the 'Messages' button.")
            messages_button.click()
            print("'Messages' button clicked.")
        except Exception as e:
            print("Failed to click 'Messages' button. Trying JavaScript click.")
            driver.execute_script("arguments[0].click();", messages_button)
            print("'Messages' button clicked using JavaScript.")   
            
            
            
            
        try:
            # Try to find the "Allow" button and click it if it exists
            wait = WebDriverWait(driver, 3)  # Wait for up to 3 seconds
            allow_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='No thanks']")))
            allow_button.click()
        except TimeoutException:
            # If the "Allow" button doesn't appear in 3 seconds, continue with the rest of the code
            print("No thanks button not found. Continuing...") 


        ###############################  END 1. Click message


        ############################### START 2. START LOOP ACROSS ALL CHATS 

        try:
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//a[@draggable='false' and contains(@class, 'messageListItem')]")
                )
            )
            while should_run['conversations']:
                total_elements = len(elements)
                print(f"Total number of elements/chats found: {total_elements}")
                
                #print("this is the first x elements", elements[:min(convs_amt, total_elements)])
                elements = elements[:min(convs_amt, total_elements)]
                for i, element in enumerate(elements): # chats 
                    print("what is should run", should_run['conversations'])
                    if not should_run['conversations']:
                        print("Stopping Messaging execution...")
                        break  # This will exit the loop and stop the execution
                    print(f"Processing element {i+1} out of {len(elements)}")
                    try:
                        element.click()
                        print(f"Chat {i+1} clicked and being processed")
                            ############################### START 3. Extract conversation
                        
                        
                        # Extract the name from the h3 tag within the clicked element
                        name_element = element.find_element(By.CSS_SELECTOR, "h3.messageListItem__name")
                        name = name_element.text
                        print(f"Name found: {name}") # This is used to save phone numbers
                        
                        
                        time.sleep(random.uniform(3, 6))
                        # Create an empty dataframe to store the datetime and text data
                        df = pd.DataFrame(columns=['datetime', 'text'])

                        # Print the total number of divs with msgHelper in their class string
                        div_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'msgHelper')]")
                        #print(f"Total number of msgHelper div elements: {len(div_elements)}")

                        for i, div in enumerate(div_elements):  # messages 
                            try:
                                print(f"\nProcessing message div element {i + 1}/{len(div_elements)}...")  # Prints which div element is being processed

                                # Debug: Print the HTML content of the div
                                #print(f"HTML content of div: {div.get_attribute('outerHTML')}")

                                # Extract the datetime value
                                time_element = div.find_element(By.TAG_NAME, "time")
                                datetime_value = time_element.get_attribute("datetime")
                                #print(f"Extracted datetime: {datetime_value}")

                                # Extract the text value
                                span_element = div.find_element(By.XPATH, ".//span[contains(@class, 'text')]")
                                text_value = span_element.text
                                #print(f"Extracted text: {text_value}")

                                # Check inner div classes
                                inner_div_elements = div.find_elements(By.TAG_NAME, "div")
                                author_value = "unknown"

                                for inner_div in inner_div_elements:
                                    inner_class = inner_div.get_attribute("class")

                                    # Debug: Print the classes of inner divs
                                    #print(f"Classes of inner div: {inner_class}")

                                    if re.search(r'\bsend\b', inner_class):
                                        author_value = "sender"
                                        break
                                    elif re.search(r'\breceive\b', inner_class):
                                        author_value = "receiver"
                                        break

                                # Append data to dataframe
                                new_row = pd.DataFrame({'datetime': [datetime_value], 'text': [text_value], 'author': [author_value]})
                                df = pd.concat([df, new_row], ignore_index=True)
                                #print(f"Appended new row to DataFrame with author {author_value}.")

                            except Exception as e:
                                print(f"An error occurred while extracting messages: {e}")



                        ############################## END 3. Extract conversation


                        ############################## START 4. GET NEXT RESPONSE FROM OPENAI 
                        # Initialize an empty list to collect rows

                        print("-------END EXTRACTING CONVO --------")
                        
                        
                        # Put option to not message older people

                        df['datetime'] = pd.to_datetime(df['datetime'])
                        last_message_datetime = df['datetime'].iloc[-1]

                        current_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # Now offset-aware
                        #days_threshold = 7  # This can be changed as needed

                        time_difference = current_datetime - last_message_datetime.to_pydatetime()
                        print(f"Last message was on {last_message_datetime}")
                        if time_difference > timedelta(days=days_threshold):

                            print(f"Skipping this iteration because the last message is more than {days_threshold} days old.")
                            continue  # Skip to the next iteration in the outer loop
                        if time_difference.total_seconds() < 30:
                            # Run some code if the time difference is less than 30 seconds
                            print("Other person's response was less than 30 seconds ago. Skip for now and respond later.")
                            continue
                        
                        
                        text_rows = []

                        # Iterate through the rows of the DataFrame
                        for _, row in df.iterrows():
                            author = row['author']
                            text = row['text']

                            # Apply the desired format based on the author
                            if author == 'sender':
                                text_rows.append(f"A: {text}")
                            elif author == 'receiver':
                                text_rows.append(f"G: {text}")

                        # Join the formatted strings to create the text
                        formatted_text = "\n".join(text_rows)

                        print("This is current convo: ", formatted_text)

                        formatted_text2 = formatted_text
                        # Split the text into lines
                        lines_dt = formatted_text2.strip().split('\n')

                        # Take the last two lines
                        last_two_lines = lines_dt[-2:]
                        
                        if len(last_two_lines) == 2 and all(line.startswith("A:") for line in last_two_lines):
                            double_texted = True
                        else:
                            double_texted = False
                        
                        if detect_phone_number(formatted_text2, name):
                            print("Passing due to phone number given.")
                            #exit() # this one works in a normal python script.
                            continue  # Use sys.exit() to terminate the entire script
                        if df.iloc[-1]['author'] == 'receiver':
                            print("The last message was by the lover so we send to OPENAI to get the next best response") 

                            # Define name of the person talkign to here:
                            #name = "G"
                            #language = 'Spanish'
                            emoji_mapping = {
                                "(wink emoji)": "😉",
                                "(smile emoji)": "😄",
                                "(sad emoji)": "😢",
                                "(heart emoji)": "❤️",
                                "(thumbs up emoji)": "😃",
                                "(smirk emoji)": "😏"  # Added smirk emoji
                                # Add more as needed
                            }
                                                        
                            # Split the text into lines
                            lines = formatted_text2.strip().split('\n')

                            # Take the first line
                            first_line = lines[0]

                            # Check if the first line contains either "Hola hermosa," or "Hello beautiful,"
                            if "bella bombón" in first_line or "Hello beautiful," in first_line:
                                # Run certain code
                                assistant_reply = simple_method(formatted_text2, name, language)
                            else:
                                # Run other code
                                assistant_reply = complex_method(formatted_text2, name, language)
                            





                        ############################## END 4. GET NEXT RESPONSE FROM OPENAI 





                            ############################## START 5. SEND THE OPENAI NEXT BEST MESSAGE

                            # Assuming 'driver' is your initialized WebDriver instance
                            actions = ActionChains(driver)
                            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
                            actions.send_keys(assistant_reply).perform()
                            print(f"Send message {assistant_reply}")
                            #time.sleep(random.uniform(20, 40))
                            actions.send_keys(Keys.RETURN)  # Sending the Enter key

                            if toggle_var.get() == 1:
                                actions.perform()  # Perform the action
                            else: 
                                print("Active Mode OFF - Message will not be sent")
                                
                            print(f"Pressed Enter") # send to open ai and get best response

                        elif time_difference > timedelta(days=4) and not double_texted: 
                            print(f"Haven't responded in {time_difference}")
                            print("She hasn't responded in more than 4 days, so do a takeaway comment")
                            if language == "Spanish":
                                assistant_reply = "Siempre eres tan habladora 😉?"
                            
                            else:
                                assistant_reply = "are you always this talkative 😉?"
                            
                            actions = ActionChains(driver)
                            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
                            actions.send_keys(assistant_reply).perform()
                            print(f"Send message {assistant_reply}")
                            #time.sleep(random.uniform(20, 40))
                            actions.send_keys(Keys.RETURN)  # Sending the Enter key

                            if toggle_var.get() == 1:
                                actions.perform()  # Perform the action
                            else: 
                                print("Active Mode OFF - Message will not be sent")
                        else:
                            print(f"Haven't responded in {time_difference}")
                            if double_texted:
                                print("Already double texted, leave it now")
                            else: 
                                print("They haven't responded yet within 4 days. Leave it more time. If 4 days passes we do a takeaway comment.")
                            continue


                        ############################## END 5. SEND THE OPENAI NEXT BEST MESSAGE
                        
                        
                        
                        
                    except Exception as e:
                        print(f"Failed to click element {i+1}: {e}")
                        driver.execute_script("arguments[0].click();", element)
                        print(f"Chat  {i+1} clicked using JavaScript.")
                
        ############################## END 2. Click the first chat 





        except Exception as e:
            print(f"An error occurred in finding the first chat: {e}")
        # Optional: Wait for any obstructing elements to disappear
        # Replace 'obstructing_element_selector' with the actual selector
        # wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, "obstructing_element_selector")))
        
        print("Conversations execution complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
    time.sleep(1)
        

       
should_run = {'first_messages': True, 'simple_conversations': True}


######## 0 LOGIN SCREEN 
# Simulate a function that checks login details (replace this with Firebase auth)
def check_login(email, password):
    # Here you would typically send these details to Firebase for verification
    return email == "user" and password == "123"


# Function to handle login
def login():
    email = email_entry.get()
    password = password_entry.get()
    
    if check_login(email, password):
        with open("login_details.json", "w") as f:
            json.dump({"email": email, "password": password}, f)
        
        messagebox.showinfo("Success", "Successfully logged in!")
        login_window.destroy()
        app.deiconify()
    else:
        messagebox.showerror("Error", "Invalid login details")

# Simulate a function that checks login details
def check_login(email, password):
    return email == "user" and password == "123"



######## 0 END LOGIN SCREEN



class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
        self.line = ""
        self.create_log_file()

    def create_log_file(self):
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
        self.log_filename = f'05-logs/log_{timestamp}.txt'
        if not os.path.exists('05-logs'):
            os.makedirs('05-logs')

    def write(self, str_):
        self.line += str_
        if '\n' in self.line:
            self.widget.config(state=tk.NORMAL)
            self.widget.insert(tk.END, self.line)
            self.widget.yview(tk.END)  # Scroll to the bottom
            self.widget.config(state=tk.DISABLED)
            with open(self.log_filename, 'a', encoding='utf-8') as f:  # Specify encoding here
                f.write(self.line)
            self.line = ""

    def flush(self):
        pass


log_area = None  # Declare a global variable to hold the log area

def show_log_window():
    global log_area  # Use the global variable
    log_window = tk.Toplevel(app)
    log_window.title("4. Observe Logs")
    
    log_area = tk.Text(log_window, height=20, width=50)
    log_area.pack(padx=5, pady=5)
    log_area.config(state=tk.DISABLED)

    sys.stdout = TextRedirector(log_area)  # Redirect stdout to the Text widget





def start_execution(func_name):
    show_log_window()  # Show log window
    should_run[func_name] = True
    print("what is should run", should_run[func_name] )
    t = Thread(target=eval(f"execute_{func_name}"))
    t.start()
    if func_name == 'first_messages':
        print("Starting first_messages...") 
        update_status_label(left_frame, status_label_left, "Starting...")
    elif func_name == 'conversations':
        print("Starting conversations...")
        update_status_label(right_frame, status_label_right, "Starting...")
    else:
        print("Starting simple conversations...")

def stop_execution(func_name):
    should_run[func_name] = False
    if func_name == 'first_messages':
        
        update_status_label(left_frame, status_label_left, "Stopping...")
        try:
            driver.quit()
        except Exception as e:
            pass
    elif func_name == 'conversations':
        update_status_label(right_frame, status_label_right, "Stopping...")
        try:
            driver.quit()
        except Exception as e:
            pass
    else:
        print("Starting simple conversations...")



def create_tooltip(widget, text):
    def on_enter(event):
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+%d+%d" % (event.x_root, event.y_root))
        ttk.Label(tooltip, text=text, background="#FFFFFF").pack()
        widget._tooltip = tooltip

    def on_leave(event):
        widget._tooltip.destroy()

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

# Initialize Tkinter App with ThemedTk
app = tk.Tk()
app.title("AutoFlirt")
app.tk.call("source", "azure.tcl")
app.tk.call("set_theme", "dark")  # or "dark" for dark theme


# app.set_theme_advanced(
#     theme_name='arc',  # Base theme
#     hue=0.15,  # Change this value to shift the hue towards red
#     brightness=1.0,  # Keep it at default
#     saturation=1.0,  # Keep it at default
#     preserve_transparency=True  # Preserves transparency
# )


# Get the background color of the app
bg_color = app.cget("background")
dark_grey = "#2A2A2A"  # Slightly darker than the original dark grey
light_grey = "#3A3A3A"   # Slightly darker than the original light grey

def toggle(event):
    if toggle_var.get() == 0:
        toggle_var.set(1)
        canvas.itemconfig(rect, fill="green")
        canvas.move(circle, 30, 0)
    else:
        toggle_var.set(0)
        canvas.itemconfig(rect, fill="red")
        canvas.move(circle, -30, 0)
        

def update_vert_line(event):
    # Update the vertical line to match the new height of the new_section_frame
    vert_line_break.coords(line, 2, 0, 2, event.height)
    #vert_line.coords(line, 2, 0, 2, event.height)



# Initialize main window


# Notebook
notebook = ttk.Notebook(app)
notebook.pack(fill=tk.BOTH, expand=True)

# Home tab
home_tab = tk.Frame(notebook, bg=bg_color)
notebook.add(home_tab, text="Home")







###### 1. Title and description #############
title_frame = tk.Frame(home_tab, bg=bg_color)
title_frame.pack(fill="x", padx=20, pady=10)

# Title
# title_label = tk.Label(title_frame, text="AutoFlirt", font=("Arial", 14), background=bg_color, anchor="w", justify="left", foreground=dark_grey)
# title_label.pack(side=tk.LEFT, fill="x")

# Toggle button
toggle_frame = tk.Frame(title_frame, bg=bg_color)
toggle_frame.pack(side=tk.RIGHT)

toggle_var = tk.IntVar(value=0)
style = ttk.Style()
style.configure('TCheckbutton', background=bg_color)

# toggle_button = ttk.Checkbutton(toggle_frame, text="Active Mode", variable=toggle_var, style='TCheckbutton')
# toggle_button.pack(side=tk.TOP)

# Toggle description
toggle_description = tk.Label(toggle_frame, text="Unchecked: Test mode - to ensure it's working\nChecked: Sends messages", wraplength=150, font=("Arial", 7), background=bg_color, anchor="e", justify="left", foreground=light_grey)
toggle_description.pack(side=tk.TOP, fill="x")

# Description
# description_label = tk.Label(home_tab, text="Automate your Tinder experience! AutoFlirt sends flirty replies, sets up dates, and collects phone numbers for you.", wraplength=400, font=("Arial", 9), background=bg_color, anchor="w", justify="left", foreground=light_grey)
# description_label.pack(fill="x", padx=20, pady=10)
###### 1. End Title and Description #########




####### 1a Line Breaker #######################

# Initialize a Canvas for the line break
line_break1a = tk.Canvas(home_tab, bg=bg_color, height=2, bd=0, highlightthickness=0)
line_break1a.pack(fill=tk.X, padx=5, pady=5)  # Add some padding around the line

def whiteraw_line_tit(event):
    line_break1a.delete("all")  # Remove the old line
    line_break1a.create_line(10, 2, event.width - 10, 2, fill="#b8b7b6", width=3)  # Create a new line with padding

line_break1a.bind("<Configure>", whiteraw_line_tit)


######### 1a. End Line Break        #########







popup_window = None  # Global variable to keep track of the popup window

def show_simple_mode_info():
    global popup_window
    if popup_window is not None:
        try:
            popup_window.focus_set()  # Bring the existing window to the front
        except tk.TclError:  # The window was closed
            popup_window = None
    if popup_window is None:
        popup_window = tk.Toplevel()
        popup_window.title("Simple Mode Info")
        
        # Create a frame to hold the labels
        frame = tk.Frame(popup_window)
        frame.pack(anchor="w")
        
        # Title for Simple Mode Not Active
        title1 = tk.Label(frame, text="Simple Mode Not Active", font=("Arial", 16), anchor="w", justify=tk.LEFT, wraplength=400, padx=10, pady=10)
        title1.pack(anchor="w")
        
        # Description for Simple Mode Not Active
        desc1 = tk.Label(frame, text="This is a more complicated conversation that aims to set up a date within 10 messages.", anchor="w", justify=tk.LEFT, wraplength=400, padx=10, pady=10)
        desc1.pack(anchor="w")
        
        # Sample longer conversation
        sample1 = tk.Label(frame, text="""
A: Hey I like your style 
G: lol thanks! you have fine taste my man
A: Just one of my many talents 😉
G: haha and what other talents do you have?
A: Well, let's just say I'm quite versatile. 
G: interesting. in what way?
A: I can adapt to any situation, whether it's climbing a mountain or trying a new cocktail.
G: lol very nice. i love cocktails
A: Then we definitely need to have a cocktail together sometime 😉
G: for sure, i'd like that
A: Great, I know this amazing bar in Madrid with the best cocktails.
G: really, where is it?
A: It's in the heart of Madrid, near the Gran Vía. You'll love it!
G: oh nice, very cool
A: We should check it out together sometime, what's your schedule like?:
G: i'm free on friday
A: Perfect Friday sounds fantastic. Shoot me your number for romantic arrangement purposes 😉
G: sure - it's 596950999
                            """, anchor="w", justify=tk.LEFT, wraplength=400, padx=10, pady=10)
        sample1.pack(anchor="w")
        
        # Title for Simple Mode Active
        title2 = tk.Label(frame, text="Simple Mode Active", font=("Arial", 16), anchor="w", justify=tk.LEFT, wraplength=400, padx=10, pady=10)
        title2.pack(anchor="w")
        
        # Description for Simple Mode Active
        desc2 = tk.Label(frame, text="This is a simple conversation that aims to set up a date within 4 messages. This is less prone to errors and is more direct.", anchor="w", justify=tk.LEFT, padx=10, pady=10)
        desc2.pack(anchor="w")
        
        # Sample Simple Mode Conversation
        sample2 = tk.Label(frame, text="""
A: Hello beautiful, I'm Ryan, how's it going?
G: Nothing, just being good at home.
A: That sounds boring, you need a distraction 😉. What do you do for fun?
G: I like to paint, and you?
A: That's great, I'm fascinated by art. I really like sports. Which part of Madrid are you from? I live near Gran Via.
G: That's good. I live in Getafe.
A: Ah, Getafe, an interesting area near Madrid. I like you, we should get together for a drink and see if we like each other. I'm not looking for anything super serious, but if you feel like having a drink, flirting, and seeing what happens, give me your number and I'll text you.
G: Okay, my number is 99999999.
                           """, anchor="w", justify=tk.LEFT, wraplength=400, padx=10, pady=10)
        sample2.pack(anchor="w")
        
        popup_window.protocol("WM_DELETE_WINDOW", on_closing_popup)


def on_closing_popup():
    global popup_window
    popup_window.destroy()
    popup_window = None



######### 2. Preferences            #########

# Preferences Title and Divider 
preferences_title = tk.Label(home_tab, text="1. Preferences", font=("Arial", 12), bg=bg_color, foreground=dark_grey)
preferences_title.pack(anchor=tk.W, padx=20, pady=5)






# Create a Canvas with the background color
canvas = tk.Canvas(home_tab, bg=bg_color, highlightthickness=0, highlightbackground=bg_color, highlightcolor=bg_color,  height=160)
canvas.pack(side=tk.TOP, padx=20, pady=5, fill=tk.BOTH)  # Changed padx to 20

# Create a Frame (tk.Frame) to add to the Canvas
preferences_frame = tk.Frame(canvas, bg=bg_color, bd=0)
canvas_frame = canvas.create_window((0, 0), window=preferences_frame, anchor=tk.NW)

# Configure column widths
preferences_frame.grid_columnconfigure(0, minsize=150)
preferences_frame.grid_columnconfigure(1, minsize=50)  # Spacer column
preferences_frame.grid_columnconfigure(2, minsize=50)  # Entry column
preferences_frame.grid_columnconfigure(3, minsize=150)  # New label column
preferences_frame.grid_columnconfigure(4, minsize=50)  # New spacer column
preferences_frame.grid_columnconfigure(5, minsize=50)  # New entry column

# For debugging
#preferences_frame.config(bg='red')
#canvas.config(bg='green')


# Short Label for Days Threshold using tk.Label
days_label = tk.Label(preferences_frame, text="Days Limit: ", bg=bg_color, font=("Arial", 10), foreground=light_grey)
days_label.grid(row=0, column=0, sticky=tk.W)#, padx=(20, 0))  # Added tuple for padx

# Entry for Days Threshold
days_entry = ttk.Entry(preferences_frame, width=20)  # Specified width
days_entry.grid(row=0, column=2, sticky=tk.E, pady=(10, 0))
days_entry.insert(0, "30")  # Default value

# Extra info under the "Days Limit" label
extra_info_label = tk.Label(preferences_frame, 
                            text="Set the maximum days since last message for replies. If the last message from someone exceeds this limit, the bot will not respond.",
                            bg=bg_color, 
                            font=("Arial", 8), 
                            wraplength=350,  # Adjust this value based on your layout
                            justify=tk.LEFT,
                            foreground=light_grey) # Text justification
extra_info_label.grid(row=1, column=0, columnspan=3, sticky=tk.W + tk.N, padx=(20, 0), pady=(0, 10))  # Added pady


# Language Selection Label using tk.Label
language_label = tk.Label(preferences_frame, text="Select Language:", bg=bg_color, font=("Arial", 10), foreground=light_grey)
language_label.grid(row=2, column=0, sticky=tk.W, padx=(20, 0), pady=(10, 0))  # Added pady and changed row to 2


# Language Selection ComboBox
language_combo = ttk.Combobox(preferences_frame, values=["English", "Spanish"], width=18)  # Specified width to match Entry
language_combo.grid(row=2, column=2, sticky=tk.E + tk.S, pady=(10, 0))  # Change row to 2
language_combo.set("English")  # Set the default value

# Extra info under the "Days Limit" label
extra_info_label_lang = tk.Label(preferences_frame, 
                            text="Set the language. The assistant automatically responds in the conversation language but selecting the language you improve the assistant's responses",
                            bg=bg_color, 
                            font=("Arial", 8), 
                            wraplength=350,  # Adjust this value based on your layout
                            justify=tk.LEFT,
                            foreground=light_grey) # Text justification
extra_info_label_lang.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=(20, 0), pady=(0, 10))  # Added pady

# Update Canvas scroll region
preferences_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox(tk.ALL))


# Short Label for Conversation Amount using tk.Label
conversations_label = tk.Label(preferences_frame, text="Conversation Amount: ", bg=bg_color, font=("Arial", 10), foreground=light_grey)
conversations_label.grid(row=0, column=3, sticky=tk.W, padx=(20, 0))

# Entry for Conversation Amount
conversations_entry = ttk.Entry(preferences_frame, width=20)  # Specified width
conversations_entry.grid(row=0, column=5, sticky=tk.E, pady=(10, 0))  # Adjusted column
conversations_entry.insert(0, "20")  # Default value

# Extra info under the "Conversation Amount" label
extra_info_label_conversations = tk.Label(preferences_frame, 
                            text="The first x conversations to interact with",
                            bg=bg_color, 
                            font=("Arial", 8), 
                            wraplength=350,  # Adjust this value based on your layout
                            justify=tk.LEFT,
                            foreground=light_grey)  # Text justification
extra_info_label_conversations.grid(row=1, column=3, columnspan=2, sticky=tk.W + tk.N, padx=(20, 0), pady=(0, 10))  # Added pady and adjusted columnspan

#style = ttk.Style()
style.configure('Circular.TButton', width=10, relief='flat', borderwidth=0)
style.map('Circular.TButton', background=[('', 'white')])  # You can set the background color here

# Create a new frame to hold both the label and the canvas
simple_mode_frame = tk.Frame(preferences_frame, bg=bg_color)
simple_mode_frame.grid(row=2, column=3, sticky=tk.W, padx=(20, 0), pady=(10, 0))

# Place the label inside the new frame
simple_mode_label = tk.Label(simple_mode_frame, text="Simple Mode: ", bg=bg_color, font=("Arial", 10), foreground=light_grey)
simple_mode_label.pack(side=tk.LEFT)



# Checkbox for Simple Mode
simple_mode_var = tk.IntVar()  # Variable to hold the checkbox state
simple_mode_checkbox = ttk.Checkbutton(preferences_frame, variable=simple_mode_var)
simple_mode_checkbox.grid(row=2, column=5, sticky=tk.E, pady=(10, 0))  # Set row to 2, same as "Select Language"

# Extra info under the "Simple Mode" label
extra_info_label_simple_mode = tk.Label(preferences_frame, 
                            text="Enable or disable simple mode. When enabled, the assistant will use simplified responses.",
                            bg=bg_color, 
                            font=("Arial", 8), 
                            wraplength=350,  # Adjust this value based on your layout
                            justify=tk.LEFT,
                            foreground=light_grey)  # Text justification
extra_info_label_simple_mode.grid(row=3, column=3, columnspan=3, sticky=tk.W + tk.N, padx=(20, 0), pady=(0, 10))  # Added pady and adjusted columnspan

# Create a Canvas widget to act as your button and place it inside the new frame
info_button_canvas = tk.Canvas(simple_mode_frame, width=20, height=20, bg=bg_color, highlightthickness=0)
info_button_canvas.pack(side=tk.LEFT)

# Draw a circle inside the canvas
info_button_canvas.create_oval(2, 2, 18, 18, fill='green', outline=bg_color)

# Add a text element inside the circle
info_button_canvas.create_text(10, 10, text='?', fill='white')

# Bind a click event to the canvas
info_button_canvas.bind("<Button-1>", lambda event: show_simple_mode_info())



preferences_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox(tk.ALL))


######### 2. End Preferences         #########



####### 2a Line Breaker #######################

# Initialize a Canvas for the line break
line_break2a = tk.Canvas(home_tab, bg=bg_color, height=2, bd=0, highlightthickness=0)
line_break2a.pack(fill=tk.X, padx=5, pady=10)  # Add some padding around the line

def whiteraw_line(event):
    line_break2a.delete("all")  # Remove the old line
    line_break2a.create_line(10, 2, event.width - 10, 2, fill="#dee0df", width=3)  # Create a new line with padding

line_break2a.bind("<Configure>", whiteraw_line)


######### 2a. End Line Break        #########

cust_title = tk.Label(home_tab, text="2. Customize conversation", font=("Arial", 12), bg=bg_color, foreground=dark_grey)
cust_title.pack(anchor=tk.W, padx=20, pady=0)


# Description
description_label_cust = tk.Label(home_tab, text="Go to the Customize tab in order to make covnersations personal to you", wraplength=400, font=("Arial", 10), background=bg_color, anchor="w", justify="left", foreground=light_grey)
description_label_cust.pack(fill="x", padx=20, pady=0)



####### 2a Line Breaker #######################

# Initialize a Canvas for the line break
line_break2b = tk.Canvas(home_tab, bg=bg_color, height=2, bd=0, highlightthickness=0)
line_break2b.pack(fill=tk.X, padx=5, pady=10)  # Add some padding around the line

def whiteraw_line(event):
    line_break2b.delete("all")  # Remove the old line
    line_break2b.create_line(10, 2, event.width - 10, 2, fill="#dee0df", width=3)  # Create a new line with padding

line_break2b.bind("<Configure>", whiteraw_line)


######### 2a. End Line Break        #########












op_title = tk.Label(home_tab, text="3. Select Operation", font=("Arial", 12), bg=bg_color, foreground=dark_grey)
op_title.pack(anchor=tk.W, padx=20, pady=10)
manual_login_var = tk.IntVar()
manual_login_button = ttk.Checkbutton(home_tab, text="First time use: Manual Log-in", variable=manual_login_var, style='TCheckbutton')
manual_login_button.pack(anchor=tk.W, padx=20, pady=5)


# Additional label for explanation
explanation_label = tk.Label(home_tab, text="Checking this box will allow manual login for first time users.", 
                             font=("Arial", 8), bg=bg_color, foreground=dark_grey)
explanation_label.pack(anchor=tk.W, padx=25, pady=2)



######### 3. START Operations New Section #########

# Preferences Title and Divider 






# Create a new Frame for the new section
new_section_frame = tk.Frame(home_tab, bg=bg_color)
new_section_frame.pack(side=tk.TOP, padx=20, pady=5, fill=tk.X)

new_section_frame.bind("<Configure>", update_vert_line)

# Create left child frame
left_frame = tk.Frame(new_section_frame, bg=bg_color, width=200)
left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)

# Vertical Line Breaker
vert_line_break = tk.Canvas(new_section_frame, bg=bg_color, width=2, bd=0, highlightthickness=0, height=100)
vert_line_break.pack(side=tk.LEFT, fill=tk.Y, padx=10)  # Add some padding around the line
line = vert_line_break.create_line(2, 0, 2, 100, fill="#dee0df", width=3)  # Create a new line with padding

# Create right child frame
right_frame = tk.Frame(new_section_frame, bg=bg_color, width=200)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

# Title and description on the left side
left_title = tk.Label(left_frame, text="a. First Messages", bg=bg_color, font=("Arial", 12), justify="center", foreground=dark_grey)
left_title.pack(anchor=tk.W, pady=5)

# Setting wraplength for left_desc
left_desc = tk.Label(left_frame, text="Sends first messages to people you have matched with.", bg=bg_color, font=("Arial", 8), justify="left", foreground=light_grey, wraplength=190)
left_desc.pack(anchor=tk.W, pady=5)


status_label_left = tk.Label(left_frame, text="", bg=bg_color, font=("Arial", 8), foreground=light_grey)
status_label_right = tk.Label(right_frame, text="", bg=bg_color, font=("Arial", 8), foreground=light_grey)

# Adding Start and Stop buttons under left_desc
# Uncomment the line below to use an image for the Start button
# start_icon_left = PhotoImage(file="start_icon.png")
# Adding Start and Stop buttons under left_desc
start_button_left = ttk.Button(left_frame, text="Start", style='Start.TButton', command=lambda: start_execution('first_messages'))
start_button_left.pack(side=tk.TOP, pady=10)

stop_button_left = ttk.Button(left_frame, text="Stop", style='Stop.TButton', command=lambda: stop_execution('first_messages'))
stop_button_left.pack(side=tk.TOP, pady=5)

status_label_left.pack_forget()  # Initially hide the status label


# Title and description on the right side
right_title = tk.Label(right_frame, text="b. Respond to Messages", bg=bg_color, font=("Arial", 12), justify="center", foreground=dark_grey)
right_title.pack(anchor=tk.W, pady=5)

# Setting wraplength for right_desc
right_desc = tk.Label(right_frame, text="Replies to received messages using our custom-trained bot.", bg=bg_color, font=("Arial", 8), justify="left", foreground=light_grey, wraplength=190)
right_desc.pack(anchor=tk.W, pady=5)

# Adding Start and Stop buttons under right_desc
start_button_right = ttk.Button(right_frame, text="Start", style='Start.TButton', command=lambda: start_execution('conversations'))
start_button_right.pack(side=tk.TOP, pady=10)

stop_button_right = ttk.Button(right_frame, text="Stop", style='Stop.TButton', command=lambda: stop_execution('conversations'))
stop_button_right.pack(side=tk.TOP, pady=5)

status_label_right.pack_forget()  # Initially hide the status label

######### 3. End New Section #########

####### 3a Line Breaker #######################

# Initialize a Canvas for the line break
line_break3a = tk.Canvas(home_tab, bg=bg_color, height=2, bd=0, highlightthickness=0)
line_break3a.pack(fill=tk.X, padx=5, pady=5)  # Add some padding around the line

def line3a_draw(event):
    line_break3a.delete("all")  # Remove the old line
    line_break3a.create_line(10, 2, event.width - 10, 2, fill="#dee0df", width=3)  # Create a new line with padding

line_break3a.bind("<Configure>", line3a_draw)

######### 3a. End Line Break #########







###### 4. Customise Tab






def show_customisation_window():
    file_path = '01-processing-files/01-split-sys-msg-method/02-getting2know-sys-msg.txt'
    profile_text = get_text_between_tags(file_path, "# Profile of A:")
    skills_text = get_text_between_tags(file_path, "# \"A\"'s skills:")
    new_window = tk.Toplevel()
    new_window.title("Customise Profile")
    new_window.configure(bg=bg_color)
    
    # Vertical line to separate the two sections
    tk.Frame(new_window, width=1, bg="gray").grid(row=0, column=1, rowspan=7, sticky="ns")

    # Title for Profile
    title1 = tk.Label(new_window, text="1. Customize profile", font=("Arial", 12), anchor="w", bg=bg_color)
    title1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Elements for Profile
    description_label1 = tk.Label(new_window, text="• Enter your profile in the text box below\n• The model will use this to personalise your conversartions\n• Talk in the second person e.g 'He is from Iceland' \n• Use the below numbered list as a guide \n\n1. Where you're from\n2. Age\n3. Past education/career info (short)\n4. Current job\n5. Hobbies\n6. Life Achievements\n7. Where you live now. \n 8.What you're looking for on the app", anchor="w", bg=bg_color, justify=tk.LEFT)  # Your text here
    description_label1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    text_entry1 = tk.Text(new_window, height=10, width=40, font=("Arial", 10))
    
    text_entry1.grid(row=2, column=0, padx=10, pady=10)
    text_entry1.insert(tk.END, profile_text)
    save_button1 = ttk.Button(new_window, text="Save Profile", command=lambda: save_profile(text_entry1, saved_label1, "# Profile of A:"))
    save_button1.grid(row=3, column=0)
    saved_label1 = tk.Label(new_window, text="", bg=bg_color)
    saved_label1.grid(row=4, column=0)
    
    # Title for Skills
    title2 = tk.Label(new_window, text="2. Customize your skills", font=("Arial", 12), anchor="w", bg=bg_color)
    title2.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    # Elements for Skills
    description_label2 = tk.Label(new_window, text="• Add your skills in Bullet point form \n• For example '* Great painter' is one bullet", anchor="w", bg=bg_color, justify=tk.LEFT)  # Your text here
    description_label2.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    text_entry2 = tk.Text(new_window, height=10, width=40, font=("Arial", 10))
    text_entry2.grid(row=2, column=2, padx=10, pady=10)
    text_entry2.insert(tk.END, skills_text)
    save_button2 = ttk.Button(new_window, text="Save Skills", command=lambda: save_profile(text_entry2, saved_label2, "# \"A\"'s skills:"))
    save_button2.grid(row=3, column=2)
    saved_label2 = tk.Label(new_window, text="", bg=bg_color)
    saved_label2.grid(row=4, column=2)
    
    
    # Second vertical line to separate the third section
    tk.Frame(new_window, width=1, bg="gray").grid(row=0, column=3, rowspan=7, sticky="ns")

    # Title for Personal Details
    title3 = tk.Label(new_window, text="3. Customize your personal details", font=("Arial", 12), anchor="w", bg=bg_color)
    title3.grid(row=0, column=4, padx=10, pady=0, sticky="w")

    # Elements for Personal Details
    # Create a frame to hold the labels and entries
    details_frame = tk.Frame(new_window, bg=bg_color)
    details_frame.grid(row=2, column=4, sticky="w", padx=10)

    # Text entry for Name
    name_label = tk.Label(details_frame, text="Name:", bg=bg_color)
    name_label.grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(details_frame, font=("Arial", 10))
    name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Text entry for City
    city_label = tk.Label(details_frame, text="City:", bg=bg_color)
    city_label.grid(row=1, column=0, sticky="w")
    city_entry = tk.Entry(details_frame, font=("Arial", 10))
    city_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    # Text entry for Area within the city
    area_label = tk.Label(details_frame, text="Area within the city:", bg=bg_color)
    area_label.grid(row=2, column=0, sticky="w")
    area_entry = tk.Entry(details_frame, font=("Arial", 10))
    area_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
    
    
    # Text entry for Area within the city
    activity_label = tk.Label(details_frame, text="An activity you do:", bg=bg_color)
    activity_label.grid(row=3, column=0, sticky="w")
    activity_entry = tk.Entry(details_frame, font=("Arial", 10))
    activity_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    
    phone_label = tk.Label(details_frame, text="Your phone number:", bg=bg_color)
    phone_label.grid(row=4, column=0, sticky="w")
    phone_entry = tk.Entry(details_frame, font=("Arial", 10))
    phone_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    
    
    name_entry.insert(0, extract_text_from_file("messages/02-cold-opener-simple-method-es.txt", "soy ", ","))
    city_entry.insert(0, extract_text_from_file("01-processing-files/02-simple-method/02a-question-tag-es.txt", "parte de ", " eres"))
    area_entry.insert(0, extract_text_from_file("01-processing-files/02-simple-method/02a-question-tag-es.txt", "Yo vivo en ", "."))
    activity_entry.insert(0, extract_text_from_file("01-processing-files/02-simple-method/02a-question-tag-es.txt", "gusta mucho", "."))
    phone_entry.insert(0, extract_text_from_file("01-processing-files/01-split-sys-msg-method/03-soft-close-mid-sys-msg-es.txt", "phone number is", "."))

    # Save button for Personal Details
    save_button3 = ttk.Button(
    new_window, 
    text="Save Personal Details (and All)", 
    command=lambda: (
        save_personal_details(name_entry, city_entry, area_entry, activity_entry, phone_entry, saved_label3),
        save_profile(text_entry2, saved_label2, "# \"A\"'s skills:"),
        save_profile(text_entry1, saved_label1, "# Profile of A:")
        )
    )

    save_button3.grid(row=3, column=4, pady=10)
    saved_label3 = tk.Label(new_window, text="", bg=bg_color)
    saved_label3.grid(row=4, column=4)

    
    
    

def show_cold_customisation__window():
    #bg_color = "#F0F0F0"
    new_window = tk.Toplevel()
    new_window.title("Customise Cold Openers")
    new_window.configure(bg=bg_color)

    # Title for Cold Openers
    title1 = tk.Label(new_window, text="1. Customize Cold Openers", font=("Arial", 12), anchor="w", bg=bg_color)
    title1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Elements for Cold Openers
    description_label1 = tk.Label(new_window, text="• Enter your cold openers below\n• Each new line should be a separate cold opener", anchor="w", bg=bg_color, justify=tk.LEFT)
    description_label1.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Dropdown for language selection
    language_var = tk.StringVar(value="English")
    language_label = tk.Label(new_window, text="Choose openers' language:", bg=bg_color)
    language_dropdown = ttk.OptionMenu(new_window, language_var, "English", "English", "Spanish")
    language_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    language_dropdown.grid(row=2, column=0, padx=200, pady=5, sticky="w")


    
    text_entry1 = tk.Text(new_window, height=10, width=40, font=("Arial", 10))
    text_entry1.grid(row=3, column=0, padx=10, pady=10)

    def load_content():
        file_name = 'messages/01-cold-openers.txt' if language_var.get() == 'English' else 'messages/01-cold-openers-es.txt'
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                text_entry1.delete(1.0, tk.END)  # Clear existing text
                text_entry1.insert(tk.END, f.read())

    load_content()
    language_var.trace("w", lambda *args: load_content())  # Reload content when language changes
 

    # Save button, move it to row 4
    save_button1 = ttk.Button(new_window, text="Save Openers", command=lambda: save_cold_opener(text_entry1, saved_label1, language_var.get()  ))
    save_button1.grid(row=4, column=0)
        
    # Save label, move it to row 5
    saved_label1 = tk.Label(new_window, text="", bg=bg_color)
    saved_label1.grid(row=5, column=0)
    

         
        


customize_tab = tk.Frame(notebook, bg=bg_color)
notebook.add(customize_tab, text="Customize")
# Create a section frame within the customize_tab
section_frame = tk.Frame(customize_tab, bg=bg_color)
section_frame.grid(row=0, column=0)

# Add title
title_label = tk.Label(section_frame, text="1. Customize your profile", bg=bg_color, font=("Arial", 12), anchor="w", justify=tk.LEFT)
title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Add description
description_label = tk.Label(
    section_frame,
    text="This is where you can customize your profile so that the conversations are tailored to your personality and your lifestyle.",
    bg=bg_color,
    wraplength=400,
    font=("Arial", 10),
    anchor="w",
    justify=tk.LEFT,
    foreground=light_grey)
description_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)

# Add button
customise_button = ttk.Button(section_frame, text="Customize", command=show_customisation_window)
customise_button.grid(row=2, column=0)

# Add horizontal line break
line_break1a = tk.Canvas(section_frame, bg=bg_color, height=2, bd=0, highlightthickness=0)
line_break1a.grid(row=3, column=0, sticky="ew", padx=5, pady=10)

# Add second title
title_label2 = tk.Label(section_frame, text="2. Customize cold openers", bg=bg_color, font=("Arial", 12), anchor="w", justify=tk.LEFT)
title_label2.grid(row=4, column=0, padx=10, pady=10, sticky="w")

# Add second description
description_label2 = tk.Label(
    section_frame,
    text="This is where you can customize cold openers for initiating conversations.",
    bg=bg_color,
    wraplength=400,
    font=("Arial", 10),
    anchor="w",
    justify=tk.LEFT,
    foreground=light_grey
)
description_label2.grid(row=5, column=0, sticky="w", padx=10, pady=10)

# Add second button
customise_openers_button = ttk.Button(section_frame, text="Customise Openers", command=show_cold_customisation__window)
customise_openers_button.grid(row=6, column=0)




#########



##### START LOG IN WINDOW ADDITIONS
def exchange_custom_token_for_id_token(custom_token):
    API_KEY = os.getenv("API_KEY") 
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={API_KEY}"
    payload = json.dumps({
        "token": custom_token,
        "returnSecureToken": True
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    id_token = response.json().get("idToken")
    return id_token


def authenticate(deiconify=True):
    email = email_entry.get()
    password = password_entry.get()
    response = requests.post('https://autoflirt-401111.ue.r.appspot.com/login', json={"email": email, "password": password}, verify=False)
    
    if response.status_code == 200:
        try:
            custom_token = response.json()['token']
            id_token = exchange_custom_token_for_id_token(custom_token)
            
            # Set the expiry time manually
            expires_in = 3600  # Firebase tokens expire in 3600 seconds (1 hour)
            expiry_time = time.time() + expires_in - 300  # Refresh 5 minutes before expiry
            
            with open('token.json', 'w') as f:
                json.dump({"idToken": id_token, "expiryTime": expiry_time}, f)
            
            # Start the token refresher thread
            threading.Thread(target=refresh_token, daemon=True).start()
            
            if deiconify:
                app.after(0, app.deiconify)
            
            login_window.destroy()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        except KeyError:
            print("Token not found in response.")
    else:
        print("Authentication failed.")

def refresh_token():
    while True:
        try:
            with open('token.json', 'r') as f:
                data = json.load(f)
                expiry_time = data.get('expiryTime', 0)
            
            # If the token is about to expire
            if time.time() >= expiry_time:
                # Re-authenticate here to get a new token
                authenticate(deiconify=False)  # This won't deiconify the main window
            
            # Wait for 5 minutes before checking again
            time.sleep(5 * 60)
        
        except Exception as e:
            print(f"An error occurred while refreshing the token: {e}")
            time.sleep(5 * 60)  # Wait for 5 minutes before trying again









# Create login window
login_window = tk.Toplevel(app)
login_window.title("Login")

# Create email and password fields
tk.Label(login_window, text="Email:").pack()
email_entry = tk.Entry(login_window)
email_entry.pack()

tk.Label(login_window, text="Password:").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

# Create login button
tk.Button(login_window, text="Login", command=authenticate).pack()
def skip_login():
    login_window.destroy()
    app.deiconify()

skip_button = tk.Button(login_window, text="Skip Login", command=skip_login)
skip_button.pack()


# Try to load saved login details
try:
    with open("login_details.json", "r") as f:
        details = json.load(f)
        email_entry.insert(0, details["email"])
        password_entry.insert(0, details["password"])
except FileNotFoundError:
    pass

###### END LOGIN WINDOW ADDITIONS



app.geometry("800x720")
app.resizable(True, True)

# screen_width = app.winfo_screenwidth()
# screen_height = app.winfo_screenheight()
# app.geometry(f"{int(screen_width * 0.4)}x{int(screen_height * 0.4)}")

app.withdraw()
app.mainloop()