import os
import tkinter as tk
from tkinter import ttk
import sys
import time
from datetime import datetime, timedelta, timezone
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
import requests
import json
from tkinter import messagebox
import firebase_admin
from firebase_admin import auth
import threading
import time 
from dotenv import load_dotenv
from cryptography.fernet import Fernet 

# Get key for decryption
# First do this with key on file - then later make it so you get it from the api end point. 
with open("key.key", "rb") as key_file:
    key = key_file.read()
cipher_suite = Fernet(key)





def count_A_lines(text):
    return sum(1 for line in text.strip().split('\n') if line.startswith("A:"))






def detect_phone_number(conversation_text, name):
    messages = [line.strip() for line in conversation_text.split('\n') if line.strip()]
    for msg in messages:
        found_number = re.findall(r'(\d{6,})', msg)
        if found_number:
            phone_number = found_number[0]
            print("Number acquired:", phone_number)

            # Format the phone number (you can modify this part to suit your specific formatting needs)
            formatted_phone_number = str(int(phone_number))  # Remove leading zeros, if any

            try:
                df_existing = pd.read_csv('03-acquirements/00-acquirements.csv')
                
                # Format the 'number' column in the existing DataFrame
                df_existing['number'] = df_existing['number'].apply(lambda x: str(int(x)))

                # Check if the number already exists
                if formatted_phone_number in df_existing['number'].values:
                    print("Number already exists. Skipping.")
                    return True
                    #continue

            except FileNotFoundError:
                df_existing = pd.DataFrame(columns=['name', 'number', 'date', 'conversation'])

            # Store to DataFrame
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df = pd.DataFrame({'name': [name], 'number': [formatted_phone_number], 'date': [now], 'conversation': [conversation_text]})
            print("Data to output: ", df)

            df = pd.concat([df_existing, df], ignore_index=True)
            
            print("Data outputted")
            df.drop_duplicates(subset=['name', 'number'], keep='first', inplace=True)
            df.to_csv('03-acquirements/00-acquirements.csv', index=False)
            return True
    return False


def contains_emoji(text):
    return bool(re.search(r'[\U0001F600-\U0001F64F]', text))


def emoji_reducer(conversation_text, assistant_reply):
    # Calculate the proportion of messages from A that contain emojis
    a_messages = [line[2:].strip() for line in conversation_text.split('\n') if line.startswith("A:")]
    total_messages = len(a_messages)
    messages_with_emojis = sum(1 for msg in a_messages if contains_emoji(msg))
    
    proportion_with_emojis = messages_with_emojis / total_messages if total_messages > 0 else 0
    print("Proportion of messages with emojis: ", proportion_with_emojis)
    # If proportion is greater than 0.25 and assistant_reply contains an emoji, remove it
    if proportion_with_emojis > 0.25 and contains_emoji(assistant_reply):
        print("Emoji removed from assistant's reply because more than 25% of 'A:' messages contained emojis.")
        assistant_reply = re.sub(r'[\U0001F600-\U0001F64F]', '', assistant_reply)
        
    return assistant_reply



def should_ask_question(conversation_text):
    a_messages = [line[2:].strip() for line in conversation_text.split('\n') if line.startswith("A:")]
    last_3_a_messages = a_messages[-3:]  # Get the last 3 messages from A

    for message in last_3_a_messages:
        if '?' in message:
            return False  # Do not ask a question if one of the last 3 messages from A contains a question mark
    return True  # Ask a question otherwise






def find_and_replace_questions(reply, day_of_week, english_question_list, spanish_question_list, language):
    sentences = re.findall(r'(A: )([\w\sÁÉÍÓÚáéíóú,\'"¿\?;:\-—\U00010000-\U0010ffff]*)', reply)
    
    questions_found = [sent for pre, sent in sentences if '?' in sent]
    
    print("This is the questions:", questions_found)
    print("this is the reply: ", reply)
    
    if questions_found:  # Check if any questions are present
        filtered_english_questions = [q for q in english_question_list if day_of_week.lower() in q.lower() or not any(day.lower() in q.lower() for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])]
        day_translation = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        
        
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

        #using_spanish = any("¿" in question for question in questions_found)
        if language=='Spanish':
            print("This is the day of the week before translation: ", day_of_week)
            day_of_week = day_translation.get(day_of_week, day_of_week)
            print("This is the day of the week after translation: ", day_of_week)
            replacement = random.choice(spanish_question_list)
            if replacement == "pregunta del dia":
                replacement = [q for q in spanish_daily_question_list if day_of_week.lower() in q.lower()][0]
        else:
            replacement = random.choice(filtered_english_questions)
            if replacement == "daily question":
                replacement = [q for q in english_daily_question_list if day_of_week.lower() in q.lower()][0]

        replacement = re.sub(r'[\U00010000-\U0010ffff]', '', replacement)
        replacement = "A: " + replacement
        
        # Replace the entire reply with the new question
        reply = replacement
    
    return reply

def remove_question(text):
    # Find the last question mark's index
    last_question_mark_index = text.rfind('?')

    # If no question mark is found, return the original text
    if last_question_mark_index == -1:
        return text

    # Find the last sentence-ending punctuation (or beginning of string) before the last question mark
    preceding_period_index = text.rfind('.', 0, last_question_mark_index)
    preceding_exclamation_index = text.rfind('!', 0, last_question_mark_index)
    
    # Take the max index among the found indices to get the closest one to the question mark
    last_sentence_ending_index = max(preceding_period_index, preceding_exclamation_index)

    if last_sentence_ending_index == -1:
        # If there's no sentence-ending punctuation, remove all text up to the question mark
        return text[last_question_mark_index + 1:].strip()
    else:
        # Otherwise, remove the text from the last sentence-ending punctuation to the question mark
        return text[:last_sentence_ending_index + 1] + text[last_question_mark_index + 1:].strip()
    
    
def get_text_between_tags(file_path, start_tag, end_tag="---"):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    in_section = False
    section_text = ""
    for line in lines:
        line = line.strip()
        if line == start_tag:
            in_section = True
        elif in_section and (line == end_tag or line == ""):
            in_section = False
        elif in_section:
            section_text += line + '\n'
    return section_text.strip()

def extract_text_from_file(filepath, start_str, end_str):
    with open(filepath, 'r') as f:
        content = f.read()
    pattern = re.escape(start_str) + r'(.*?)' + re.escape(end_str)
    match = re.search(pattern, content)
    if match:
        try:
            return match.group(1).strip().encode('latin1').decode('utf-8')
        except:
            return match.group(1).strip()
    return ""



def save_personal_details(name_entry, city_entry, area_entry, activity_entry, phone_entry, label_widget):
    # 1. For the name entry
    name = name_entry.get()
    for filename in ["02-cold-opener-simple-method-es.txt", "02-cold-opener-simple-method.txt"]:
        filepath = f"messages/template-version/{filename}"
        with open(filepath, 'r') as f:
            content = f.read()
        content = content.replace("[Name]", name)
        with open(f"messages/{filename}", 'w') as f:
            f.write(content)

    # 2. For the city entry
    city = city_entry.get()
    pnumber = phone_entry.get()
    files_to_update = [
        "01-opener-sys-msg-es.txt",
        "01-opener-sys-msg.txt",
        "02-getting2know-sys-msg-es.txt",
        "02-getting2know-sys-msg.txt",
        "03-soft-close-mid-sys-msg-es.txt",
        "03-soft-close-mid-sys-msg.txt",
        "03a-soft-close-detector-mid-sys-msg-es.txt",
        "03a-soft-close-detector-mid-sys-msg.txt",
        "04-hard-close-sys-msg-es.txt",
        "04-hard-close-sys-msg.txt"
    ]
    for filename in files_to_update:
        filepath = f"01-processing-files/01-split-sys-msg-method/template-version/{filename}"
        with open(filepath, 'r') as f:
            content = f.read()
        #print("city is: ", city)
        #print("content before")
        #print(content)
        content = content.replace("[city]", city)
        content = content.replace("[pnumber]", pnumber)
        #print("content after")
        #print(content)
        with open(f"01-processing-files/01-split-sys-msg-method/{filename}", 'w') as f:
            f.write(content)

    # 3. For the area entry
    area = area_entry.get()
    # for filename in ["02a-question-tag-es.txt", "02a-question-tag.txt"]:
    #     filepath = f"01-processing-files/02-simple-method/template-version/{filename}"
    #     with open(filepath, 'r') as f:
    #         content = f.read()
    #     content = content.replace("[area]", area)
    #     with open(f"01-processing-files/02-simple-method/{filename}", 'w') as f:
    #         f.write(content)

    #4. For the activity entry (Note: activity_entry is not defined in your snippet)

    activity = activity_entry.get()
    for filename in ["02a-question-tag-es.txt", "02a-question-tag.txt",
                     "02-que-haces-pa-divertirte-response.txt",
                     "02-que-haces-pa-divertirte-response-es.txt",
                     "03-de-donde-eres-es.txt",
                     "03-de-donde-eres.txt"]:
        filepath = f"01-processing-files/02-simple-method/template-version/{filename}"
        with open(filepath, 'r') as f:
            content = f.read()
        content = content.replace("[activity]", activity)
        content = content.replace("[area]", area)
        content = content.replace("[city]", city)
        content = content.replace("[pnumber]", pnumber)
        with open(f"01-processing-files/02-simple-method/{filename}", 'w') as f:
            f.write(content)

    # 5. Show "Saved!"
    label_widget.config(text="Saved!")
    
    

def fix_text(text):
    replacements = {
        'ã¡': 'á',
        'ã©': 'é',
        'ã­': 'í',
        'ã³': 'ó',
        'ãº': 'ú',
        'ã±': 'ñ',
        'ã¼': 'ü',
        'ã€': 'à',
        'ã¨': 'è',
        'ã¬': 'ì',
        'ã²': 'ò',
        'ã¹': 'ù',
        'ã¢': 'â',
        'ãª': 'ê',
        'ã®': 'î',
        'ã´': 'ô',
        'ã»': 'û',
        'ã¤': 'ä',
        'ã«': 'ë',
        'ã¯': 'ï',
        'ã¶': 'ö',
        'ã¼': 'ü',
        'ã¿': 'ÿ',
        # Add more replacements here
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text



def get_response(messages):
    url = "https://us-central1-autoflirt-401111.cloudfunctions.net/openai_proxy"
    
    # Read the token from the local file
    try:
        with open('token.json', 'r') as f:
            data = json.load(f)
            id_token = data['idToken']
    except FileNotFoundError:
        return {"error": "Token file not found"}
    
    headers = {
        'Authorization': f'{id_token}'
    }
    
    data = {
        "messages": messages  # Use the messages variable here
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        
        if response.status_code == 200:
            response_json = response.json()
            return response_json
    except requests.RequestException as e:
        return {"error": f"An error occurred: {str(e)}"}

def update_status_label(frame, label, text):
    label.config(text=text)
    label.pack(side=tk.TOP, pady=5)
    frame.update()


def save_cold_opener(text_widget, label_widget, language):
    file_name = 'messages/01-cold-openers.txt' if language == 'English' else 'messages/01-cold-openers-es.txt'
    content = text_widget.get("1.0", tk.END)
    with open(file_name, 'w') as f:
        f.write(content)
    label_widget.config(text="Saved!")


def save_profile(text_entry, saved_label, marker_text):
    folder_path = "01-processing-files/01-split-sys-msg-method"
    files_to_update = [
        "01-opener-sys-msg-es.txt",
        "01-opener-sys-msg.txt",
        "02-getting2know-sys-msg-es.txt",
        "02-getting2know-sys-msg.txt",
        "03-soft-close-mid-sys-msg-es.txt",
        "03-soft-close-mid-sys-msg.txt",
        "03a-soft-close-detector-mid-sys-msg-es.txt",
        "03a-soft-close-detector-mid-sys-msg.txt",
        "04-hard-close-sys-msg-es.txt",
        "04-hard-close-sys-msg.txt"
    ]
    
    new_text = text_entry.get("1.0", "end-1c")
    
    for file_name in files_to_update:
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        start_line = None
        end_line = None
        for i, line in enumerate(lines):
            if marker_text in line:
                start_line = i + 1
            elif line.strip() == "" and start_line is not None:
                end_line = i
                break
        
        if start_line is not None and end_line is not None:
            del lines[start_line:end_line]
            lines.insert(start_line, new_text + "\n")
        
        with open(file_path, 'w') as f:
            f.writelines(lines)
    
    folder_path = "01-processing-files/02-simple-method"
    files_to_update = [
        "01-opener-sys-msg-es.txt",
        "01-opener-sys-msg.txt",
        "02-que-haces-pa-divertirte-response-es.txt",
        "02-que-haces-pa-divertirte-response.txt",
        "03-de-donde-eres-es.txt",
        "03-de-donde-eres.txt"
    ]
    
    new_text = text_entry.get("1.0", "end-1c")
    
    for file_name in files_to_update:
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        start_line = None
        end_line = None
        for i, line in enumerate(lines):
            if marker_text in line:
                start_line = i + 1
            elif line.strip() == "" and start_line is not None:
                end_line = i
                break
        
        if start_line is not None and end_line is not None:
            del lines[start_line:end_line]
            lines.insert(start_line, new_text + "\n")
        
        with open(file_path, 'w') as f:
            f.writelines(lines)
    
    saved_label.config(text="Saved!")
 
    
def save_all_details(name_entry, city_entry, area_entry, activity_entry, phone_entry, text_entry1, text_entry2, saved_label3):
    # Fetch the values from the entry boxes and text fields
    name = name_entry.get()
    city = city_entry.get()
    area = area_entry.get()
    activity = activity_entry.get()
    phone = phone_entry.get()
    profile_text = text_entry1.get("1.0", tk.END).strip()  # From line 1 to end
    skills_text = text_entry2.get("1.0", tk.END).strip()  # From line 1 to end

    # Prepare the text to be written to the file
    text_to_save = f"""Profile:
{profile_text}
---
Skills:
{skills_text}
---
Name:
{name}
---
City:
{city}
---
Area within the city you live:
{area}
---
An activity you do:
{activity}
---
Your phone number:
{phone}
"""

    # Write to file
    with open('personal_details.txt', 'w') as file:
        file.write(text_to_save)

    # Update the label to show that the information was saved
    saved_label3.config(text="Saved!")


    
def complex_method(formatted_text2, name, language):
    emoji_mapping = {
    "(wink emoji)": "😉",
    "(smile emoji)": "😄",
    "(sad emoji)": "😢",
    "(heart emoji)": "❤️",
    "(thumbs up emoji)": "😃",
    "(smirk emoji)": "😏"  # Added smirk emoji
    # Add more as needed
    }
    print("This is the formatted_text2:", formatted_text2)
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



    try:
        # Try to detect the language
        detected_lang = detect(g_lines)
        print("Detected lang is:", detected_lang)
        
        if detected_lang in ['es', 'nl', 'sl', 'ca']:
            language = "Spanish"
            print("Spanish detected. Conv will be in Spanish")
        else:
            language = "English"
            print("English detected. Conv will be in English")
            
    except Exception as e:
        # If an error occurs in detection, print the error and continue
        print(f"An error occurred: {e}")
        print("Continuing without changing the language.")


    # if detect_phone_number(formatted_text2, name):
    #     print("Exiting due to phone number.")
    #     #exit() # this one works in a normal python script.
    #     sys.exit(0)  # Use sys.exit() to terminate the entire script


    # Check if the application is packaged
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))


    print("Conv will be in: ", language)

    # Define parameterized variables at the top for easy modification
    if language != 'Spanish':
        #OPENER_FILE = "01-processing-files/01-split-sys-msg-method/01-opener-sys-msg.txt"
        OPENER_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '01-opener-sys-msg.txt.enc')
        #GETTING_TO_KNOW_FILE = "01-processing-files/01-split-sys-msg-method/02-getting2know-sys-msg.enc"
        GETTING_TO_KNOW_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '02-getting2know-sys-msg.txt.enc')
        #SOFT_CLOSE_MID_FILE = "01-processing-files/01-split-sys-msg-method/03-soft-close-mid-sys-msg.enc"
        SOFT_CLOSE_MID_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '03-soft-close-mid-sys-msg.txt.enc')
        #HARD_CLOSE_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg.enc"
        HARD_CLOSE_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '04-hard-close-sys-msg.txt.enc')
    else:
        # OPENER_FILE = "01-processing-files/01-split-sys-msg-method/01-opener-sys-msg-es.enc"
        # GETTING_TO_KNOW_FILE = "01-processing-files/01-split-sys-msg-method/02-getting2know-sys-msg-es.enc"
        # SOFT_CLOSE_MID_FILE = "01-processing-files/01-split-sys-msg-method/03-soft-close-mid-sys-msg-es.enc"
        # HARD_CLOSE_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg-es.enc"
        #OPENER_FILE = "01-processing-files/01-split-sys-msg-method/01-opener-sys-msg.enc"
        OPENER_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '01-opener-sys-msg-es.txt.enc')
        #GETTING_TO_KNOW_FILE = "01-processing-files/01-split-sys-msg-method/02-getting2know-sys-msg.enc"
        GETTING_TO_KNOW_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '02-getting2know-sys-msg-es.txt.enc')
        #SOFT_CLOSE_MID_FILE = "01-processing-files/01-split-sys-msg-method/03-soft-close-mid-sys-msg.enc"
        SOFT_CLOSE_MID_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '03-soft-close-mid-sys-msg-es.txt.enc')
        #HARD_CLOSE_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg.enc"
        HARD_CLOSE_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '04-hard-close-sys-msg-es.txt.enc')
 















    # Configure OpenAI API client
    # openai_api_key = os.path.join(application_path, '00-credentials', '00-openai-key.txt')
    # #openai_api_key = "00-credentials/00-openai-key.txt"
    # with open(openai_api_key, "r") as f:
    #     api_key = f.read().strip()

    #openai.api_key = api_key

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
        soft_close_detector = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '03a-soft-close-detector-mid-sys-msg.txt.enc')
        #soft_close_detector = "01-processing-files/01-split-sys-msg-method/03a-soft-close-detector-mid-sys-msg.txt"
        with open(soft_close_detector, "rb") as f:  # Note the "rb" for reading in binary mode
            encrypted_data = f.read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            temp_system_message = decrypted_data.decode().strip()  # Decoding bytes to string and then stripping

            
        temp_system_message = replace_tags(temp_system_message)
        content = '{prompt}: \n "{text}"'.format(prompt=temp_system_message, text=formatted_text2)
        messages = [{"role": "user", "content": content}]
        response = get_response(messages)
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
    print("We're at just before the file is decrypted")
    with open(system_message_file, "rb") as f:  # Note the "rb" for reading in binary mode
        encrypted_data = f.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        system_message = decrypted_data.decode().strip()  # Decoding bytes to string and then stripping
        print("System message decryted successfully.")
    
    

        
    # Get the current day
    current_day = datetime.now().strftime('%A')  # This will give you the day like 'Monday', 'Tuesday', etc.

    # Replace "[today]" with the current day in the system_message
    if "Today is [today]" in system_message:
        system_message = system_message.replace("[today]", current_day)
    if "[gname]" in system_message:
        system_message = system_message.replace("[gname]", name)
        
    

    # Define the messages list with the {text} field
    system_message = replace_tags(system_message)
    print("This is the system message: ", system_message)
    content = '{prompt}: \n "{text}"'.format(prompt=system_message, text=formatted_text2)
    messages = [{"role": "user", "content": content}]

    # Use openai.ChatCompletion.create() with the updated messages list
    while True:
        # Use openai.ChatCompletion.create() with the updated messages list
        response = get_response(messages)
        

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
    emoji_mapping = {
    "(wink emoji)": "😉",
    "(smile emoji)": "😄",
    "(sad emoji)": "😢",
    "(heart emoji)": "❤️",
    "(thumbs up emoji)": "😃",
    "(smirk emoji)": "😏"  # Added smirk emoji
    # Add more as needed
    }

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
    # if language != 'Spanish':
    #     OPENER_FILE = "01-processing-files/02-simple-method/01-opener-sys-msg.txt"
    #     second_message = "01-processing-files/02-simple-method/02-que-haces-pa-divertirte-response.txt"
    #     third_message = "01-processing-files/02-simple-method/03-de-donde-eres.txt"
    #     GETTING_TO_KNOW_FILE = "01-processing-files/01-split-sys-msg-method/02-getting2know-sys-msg.txt"
    #     SOFT_CLOSE_MID_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg.txt"
    #     HARD_CLOSE_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg.txt"
    # else:
    #     OPENER_FILE = "01-processing-files/02-simple-method/01-opener-sys-msg-es.txt"
    #     second_message = "01-processing-files/02-simple-method/02-que-haces-pa-divertirte-response-es.txt"
    #     third_message = "01-processing-files/02-simple-method/03-de-donde-eres-es.txt"
    #     GETTING_TO_KNOW_FILE = "01-processing-files/01-split-sys-msg-method/02-getting2know-sys-msg-es.txt"
    #     SOFT_CLOSE_MID_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg-es.txt"
    #     HARD_CLOSE_FILE = "01-processing-files/01-split-sys-msg-method/04-hard-close-sys-msg-es.txt"
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
        
    if language != 'Spanish':
        OPENER_FILE = os.path.join(application_path, '01-processing-files', '02-simple-method', '01-opener-sys-msg.txt.enc')
        second_message = os.path.join(application_path, '01-processing-files', '02-simple-method', '02-que-haces-pa-divertirte-response.txt.enc')
        third_message = os.path.join(application_path, '01-processing-files', '02-simple-method', '03-de-donde-eres.txt.enc')
        GETTING_TO_KNOW_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '02-getting2know-sys-msg.txt.enc')
        SOFT_CLOSE_MID_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '04-hard-close-sys-msg.txt.enc')
        HARD_CLOSE_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '04-hard-close-sys-msg.txt.enc')
    else:
        OPENER_FILE = os.path.join(application_path, '01-processing-files', '02-simple-method', '01-opener-sys-msg-es.txt.enc')
        second_message = os.path.join(application_path, '01-processing-files', '02-simple-method', '02-que-haces-pa-divertirte-response-es.txt.enc')
        third_message = os.path.join(application_path, '01-processing-files', '02-simple-method', '03-de-donde-eres-es.txt.enc')
        GETTING_TO_KNOW_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '02-getting2know-sys-msg-es.txt.enc')
        SOFT_CLOSE_MID_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '04-hard-close-sys-msg-es.txt.enc')
        HARD_CLOSE_FILE = os.path.join(application_path, '01-processing-files', '01-split-sys-msg-method', '04-hard-close-sys-msg-es.txt.enc')













    # Configure OpenAI API client
    # #openai_api_key = "00-credentials/00-openai-key.txt"
    # openai_api_key = os.path.join(application_path, '00-credentials', '00-openai-key.txt')
    # with open(openai_api_key, "r") as f:
    #     api_key = f.read().strip()

    #openai.api_key = api_key

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

        with open("01-processing-files/01-split-sys-msg-method/03a-soft-close-detector-mid-sys-msg.txt.enc", "rb") as f:  # Note the "rb" for reading in binary mode
            encrypted_data = f.read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            temp_system_message = decrypted_data.d
            
        if "Today is [today]" in system_message:
            temp_system_message = temp_system_message.replace("[today]", current_day)
        temp_system_message = replace_tags(temp_system_message)
        content = '{prompt}: \n "{text}"'.format(prompt=temp_system_message, text=formatted_text2)
        messages = [{"role": "user", "content": content}]
        response = get_response(messages)

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

    with open(system_message_file, "rb") as f:  # Note the "rb" for reading in binary mode
        encrypted_data = f.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        system_message_file = decrypted_data.decode().strip()  # Decoding bytes to string and then stripping

    if "Today is [today]" in system_message:
        system_message = system_message.replace("[today]", current_day)
    if "[gname]" in system_message:
        system_message = system_message.replace("[gname]", name)
    # Define the messages list with the {text} field
    system_message = replace_tags(system_message)
    content = '{prompt}: \n "{text}"'.format(prompt=system_message, text=formatted_text2)
    messages = [{"role": "user", "content": content}]

    # Use openai.ChatCompletion.create() with the updated messages list
    while True:
        # Use openai.ChatCompletion.create() with the updated messages list
        response = get_response(messages)


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
        #question_tag = '01-processing-files/02-simple-method/02a-question-tag-es.txt'
        question_tag_2a = os.path.join(application_path, '01-processing-files', '02-simple-method', '02a-question-tag-es.txt.enc')
        # with open(question_tag_2a, 'r', encoding='utf-8') as file:
        #     file_content = file.read()
        with open(question_tag_2a, "rb") as f:  # Note the "rb" for reading in binary mode
            encrypted_data = f.read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            file_content = decrypted_data.decode().strip()  # Decoding bytes to string and then stripping


        # Append the content to assistant_reply
        assistant_reply += " " + file_content    

    if system_message_file == third_message:
        print("reply third msg" ,assistant_reply)
        if not assistant_reply.strip().endswith('.') and not assistant_reply.strip().endswith('?'):
            assistant_reply = assistant_reply.strip() + '.'

        # Read the content from the file
        #question_tag = '01-processing-files/02-simple-method/03a-question-tag-es.txt'
        question_tag = os.path.join(application_path, '01-processing-files', '02-simple-method', '03a-question-tag-es.txt.enc')
        # with open(question_tag, 'r', encoding='utf-8') as file:
        #     file_content = file.read()
        with open(question_tag, "rb") as f:  # Note the "rb" for reading in binary mode
            encrypted_data = f.read()
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            file_content = decrypted_data.decode().strip()  # Decoding bytes to string and then stripping



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


def execute_first_messages(should_run, toggle_var, manual_login_var, simple_mode_var, language_combo, days_entry, conversations_entry):


    language = language_combo.get()
    print("Language is:", language)
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
                
        if not should_run['first_messages']:
            print("Stopping First Messages execution...")
            try:
                driver.quit()
            except:
                pass
            return  # This will exit the function immediately

        
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
        if not should_run['first_messages']:
            print("Stopping First Messages execution...")
            try:
                driver.quit()
            except:
                pass
            return  # This will exit the function immediately        
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


        if not should_run['first_messages']:
            print("Stopping First Messages execution...")
            try:
                driver.quit()
            except:
                pass
            return  # This will exit the function immediately

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

        
        if not should_run['first_messages']:
            print("Stopping First Messages execution...")
            try:
                driver.quit()
            except:
                pass
            return  # This will exit the function immediately
        
        ###############################  END 1. Click matches
            

            
        ############################### START 1a. Get the amount of matches  
            
        # Find all 'li' elements on the page with the specific style
        li_elements_with_style = driver.find_elements(By.XPATH, "//li[@style='width: 33.33%;']")

        # Get the count of such 'li' elements
        count_of_li_with_style = len(li_elements_with_style)

        # Print the count
        print(f"Number of li elements with style='width: 33.33%;': {count_of_li_with_style}")


        if not should_run['first_messages']:
            print("Stopping First Messages execution...")
            try:
                driver.quit()
            except:
                pass
            return  # This will exit the function immediately       

        ############################### END 1a. Get the amount of matches 



        ############################### START 1b. Determine if user has gold or not


        try:
            element = driver.find_element(By.XPATH, "//*[contains(@class, 'ds-background-gold')]")
            first_match = 3
        except NoSuchElementException:
            first_match = 2

        if not should_run['first_messages']:
            print("Stopping First Messages execution...")
            try:
                driver.quit()
            except:
                pass
            return  # This will exit the function immediately
        

        ############################### END 1b. Determine if user has gold or not






        for i in range(count_of_li_with_style):
            if not should_run['first_messages']:
                print("Stopping First Messages execution...")
                try:
                    driver.quit()
                except:
                    pass
                break  # This will exit the loop and stop the execution# messages 
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


            if not should_run['first_messages']:
                print("Stopping First Messages execution...")
                try:
                    driver.quit()
                except:
                    pass
                break  # This will exit the loop and stop the execution# messages 

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
                
            if not should_run['first_messages']:
                print("Stopping First Messages execution...")
                try:
                    driver.quit()
                except:
                    pass
                break  # This will exit the loop and stop the execution# messages 
            






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
            random_line = replace_tags(random_line)
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


            if not should_run['first_messages']:
                print("Stopping First Messages execution...")
                try:
                    driver.quit()
                except:
                    pass
                break  # This will exit the loop and stop the execution# messages 
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


            if not should_run['first_messages']:
                print("Stopping First Messages execution...")
                try:
                    driver.quit()
                except:
                    pass
                break  # This will exit the loop and stop the execution# messages 
            ############################### END  4. Need to go back to matches to send more colds



        #how many lis are there - that's the length of the loop. 

        # Close the driver but don't delete the profile
        print("That's all the messages done for now")
        driver.quit()

        print("First messages execution complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
    time.sleep(1)

def execute_conversations(should_run, toggle_var, manual_login_var, simple_mode_var, language_combo, days_entry, conversations_entry):


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
        
        if not should_run['conversations']:
            print("Stopping Conversations execution...")
            try:
                driver.quit()
            except:
                pass
            return # This will exit the loop and stop the execution# messages 



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
        if not should_run['conversations']:
            print("Stopping Conversations execution...")
            try:
                driver.quit()
            except:
                pass
            return # This will exit the loop and stop the execution# messages            
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
        if not should_run['conversations']:
            print("Stopping Conversations execution...")
            try:
                driver.quit()
            except:
                pass
            return # This will exit the loop and stop the execution# messages 
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
                        print("Stopping Conversations execution...")
                        try:
                            driver.quit()
                        except:
                            pass
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

                        for i, div in enumerate(div_elements):
                            if not should_run['conversations']:
                                print("Stopping Conversations execution...")
                                try:
                                    driver.quit()
                                except:
                                    pass
                                break  # This will exit the loop and stop the execution# messages 
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
                        if not should_run['conversations']:
                            print("Stopping Conversations execution...")
                            try:
                                driver.quit()
                            except:
                                pass
                            break  # This will exit the loop and stop the execution# messages 
                        
                        
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
                                print("Simple method used")
                                assistant_reply = simple_method(formatted_text2, name, language)
                            else:
                                # Run other code
                                print("Complex method used")
                                assistant_reply = complex_method(formatted_text2, name, language)
                            





                        ############################## END 4. GET NEXT RESPONSE FROM OPENAI 





                            ############################## START 5. SEND THE OPENAI NEXT BEST MESSAGE

                            # Assuming 'driver' is your initialized WebDriver instance
                            if not should_run['conversations']:
                                print("Stopping Conversations execution...")
                                try:
                                    driver.quit()
                                except:
                                    pass
                                break  # This will exit the loop and stop the execution# messages 
                            assistant_reply = replace_tags(assistant_reply)
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
        
def replace_tags(system_message):
    # Step 1: Read the file
    with open('personal_details.txt', 'r') as f:
        file_content = f.read()

    # Step 2: Split content by '---'
    sections = file_content.strip().split('---')

    # Step 3: Create a dictionary to store the text under each heading
    details_dict = {}
    for section in sections:
        lines = section.strip().split('\n')
        key = lines[0].strip().lower().replace(":", "")  # Remove the colon and convert to lower case
        value = "\n".join(lines[1:]).strip()  # The rest of the lines form the value
        details_dict[key] = value

    # Step 4: Replace the tags in the system_message
    tags_to_replace = {
        '[profile]': details_dict.get('profile', 'Error: Profile not found'),
        '[skills]': details_dict.get('skills', 'Error: Skills not found'),
        '[city]': details_dict.get('city', 'Error: City not found'),
        '[area]': details_dict.get('area within the city you live', 'Error: Area not found'),
        '[activity]': details_dict.get('an activity you do', 'Error: Activity not found'),
        '[pnumber]': details_dict.get('your phone number', 'Error: Phone number not found'),
        '[Name]': details_dict.get('name', 'Error: Phone number not found')
    }

    for tag, replacement in tags_to_replace.items():
        system_message = system_message.replace(tag, replacement)

    return system_message

