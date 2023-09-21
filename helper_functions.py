import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import numpy as np
import pandas as pd
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from google_auth_oauthlib import flow
import openai
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time  # Import the time module
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import ast
import os
import gspread
from gspread_dataframe import set_with_dataframe
import selenium
import pandas as pd
from datetime import datetime, timedelta
import ast
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from datetime import timedelta, datetime
from google.cloud import storage
from git import Repo, Git
import random
import pickle
from selenium.webdriver.common.action_chains import ActionChains
import openai
import json
from datetime import datetime
import pandas as pd
import platform
import subprocess
import stat
import openai
import sys
import re
import os
from selenium import webdriver
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
import os
from selenium import webdriver


def count_A_lines(text):
    return sum(1 for line in text.strip().split('\n') if line.startswith("A:"))



def detect_phone_number(conversation_text, name):
    messages = [line.strip() for line in conversation_text.split('\n') if line.strip()] 
    for msg in messages:
        found_number = re.findall(r'(\d{6,})', msg)
        if found_number:
            phone_number = found_number[0]
            print("Number acquired:", phone_number)

            # Store to CSV
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df = pd.DataFrame({'name': [name], 'number': [phone_number], 'date': [now]})
            print("Data to output: ", df)
            
            try:
                df_existing = pd.read_csv('03-acquirements/00-acquirements.csv')
                df = pd.concat([df_existing, df], ignore_index=True)
            except FileNotFoundError:
                pass

            print("Data outputted")
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



def find_and_replace_questions(reply, day_of_week, english_question_list, spanish_question_list):
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

        using_spanish = any("¿" in question for question in questions_found)
        if using_spanish:
            day_of_week = day_translation.get(day_of_week, day_of_week)
            replacement = random.choice(spanish_question_list)
            if replacement == "pregunta del dia":
                replacement = [q for q in spanish_question_list if day_of_week.lower() in q.lower()][0]
        else:
            replacement = random.choice(filtered_english_questions)
            if replacement == "daily question":
                replacement = [q for q in english_question_list if day_of_week.lower() in q.lower()][0]

        replacement = re.sub(r'[\U00010000-\U0010ffff]', '', replacement)
        replacement = "A: " + replacement
        
        # Replace the entire reply with the new question
        reply = replacement
    
    return reply