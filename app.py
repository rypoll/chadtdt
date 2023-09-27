import tkinter as tk
from tkinter import ttk
#from tkinter import messagebox
import sys
#import numpy as np
import pandas as pd
#import json
#from googleapiclient.discovery import build
#from google.oauth2.credentials import Credentials
#import base64
#from google_auth_oauthlib import flow
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
#import ast
import os
#import gspread
from gspread_dataframe import set_with_dataframe
#import selenium
import pandas as pd
from datetime import datetime, timedelta
#import ast
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from datetime import timedelta, datetime
#from google.cloud import storage
#from git import Repo, Git
import random
#import pickle
from selenium.webdriver.common.action_chains import ActionChains
import openai
#import json
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
from helper_functions import detect_phone_number, contains_emoji, emoji_reducer, should_ask_question, find_and_replace_questions, count_A_lines
import tkinter as tk
from tkinter import ttk
from threading import Thread
#import sv_ttk
from ttkthemes import ThemedTk 
#from tkinter import PhotoImage
import platform
#import ctypes
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from tkinter import simpledialog




chromedriver_path = r'04-assets\\chromedriver.exe'
extension_path2 = r'04-assets\\uBlock-Origin.crx'
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_extension(extension_path2)
chrome_options.add_argument('--start-maximized') 



class RedirectStdout:
    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)

    def flush(self):
        pass  # Add a flush method to avoid the error




def update_status_label(frame, label, text):
    label.config(text=text)
    label.pack(side=tk.TOP, pady=5)
    frame.update()







def execute_first_messages():
    language = language_combo.get()
    try:
        #print("Executing first messages...")
        chromedriver_path = r'04-assets\\chromedriver.exe'
        extension_path2 = r'04-assets\\uBlock-Origin.crx'
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_extension(extension_path2)
        chrome_options.add_argument('--start-maximized') 
                

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

        
        chrome_options.add_argument(f"user-data-dir={profile_directory}")

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

        # service = webdriver.chrome.service.Service(executable_path=chromedriver_path)
        # service.start()
        # driver = webdriver.Chrome(options=chrome_options)
        time.sleep(random.uniform(3, 6))
        # Open the website
        driver.get('https://www.tinder.com/')

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
            
            ###############################  START 2. Click First Match

            print(f"Locating the {i} 'li' in the first 'ul'.")
            third_li = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//ul)[1]/li[{first_match}]")))

            try:
                print(f"Clicking the {i} 'li'.")
                third_li.click()
                print(f"{i} 'li' clicked.")
            except Exception as e:
                print(f"Failed to click {i} 'li': {e}. Trying JavaScript click.")
                driver.execute_script("arguments[0].click();", third_li)
                print(f"{i} 'li' clicked using JavaScript.")




            ###############################  END 2. Click First Match 







            ################################ START  3. Cold Opener Text and Send

            # Assuming 'driver' is your WebDriver instance
            time.sleep(random.uniform(3, 6))
            # Read the file into a list
            if language == 'Spanish':
                with open('messages/01-cold-openers-es.txt', 'r') as file:
                    lines = file.readlines()
            else: 
                with open('messages/01-cold-openers.txt', 'r') as file:
                    lines = file.readlines()
                

            # Remove any leading/trailing whitespace from each line
            lines = [line.strip() for line in lines]

            # Randomly pick a line from the list
            random_line = random.choice(lines)

            # Assuming 'driver' is your initialized WebDriver instance
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()

            actions.send_keys(random_line).perform()
            print(f"Send message {random_line}")
            time.sleep(random.uniform(3, 6))
            actions.send_keys(Keys.RETURN)  # Sending the Enter key

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
            first_match+=1  


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
        chrome_options.add_argument(f"user-data-dir={profile_directory}")

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
                    
                    
                    
                    
                    
                    
        # Open the website
        driver.get('https://www.tinder.com/')

        # If it's the first time or the directory was empty, ask the user to log in manually

        #time.sleep(60)  # 60 seconds, change it to the time you need

        print("Waiting for 'Messages' button to appear.")
        if manual_login_var.get() == 1 :
            print("First time user detected - you must log in.")
            print("After first time log in you need not log in again.")
            wait = WebDriverWait(driver, 120)
            messages_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Messages']")))
        else:
            wait = WebDriverWait(driver, 20)
            messages_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Messages']")))



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
            total_elements = len(elements)
            print(f"Total number of elements found: {total_elements}")

            for i, element in enumerate(elements): # chats 
                if not should_run['first_messages']:
                    print("Stopping Messaging execution...")
                    break  # This will exit the loop and stop the execution
                print(f"Processing element {i+1} out of {total_elements}")
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
                    
                    
                    if detect_phone_number(formatted_text2, name):
                        print("Passing due to phone number given.")
                        #exit() # this one works in a normal python script.
                        continue  # Use sys.exit() to terminate the entire script
                    if df.iloc[-1]['author'] == 'receiver':
                        print("The last message was by the lover so we send to OPENAI to get the next best response") 

                        # Define name of the person talkign to here:
                        #name = "G"
                        language = 'Spanish'










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
                            "daily question",
                            "How goes your funday sunday?",
                            "How goes your taco tuesday?",
                            "How's your Mocha Monday treating you?",
                            "How's your wonderful wednesday?",
                            "How's your thirsty Thursday treating you?",
                            "How's your Fabulous Friday going?",
                            "How goes your soulful Saturday?",
                            "How's your sunday funday?"
                        ]

                        spanish_question_list = [
                            "de donde eres originalmente?",
                            "pregunta del dia",
                            "Cómo te trata el Lunes de Lujo?",
                            "Cómo va tu Martes Maravilloso?",
                            "Cómo te va en el Miércoles Melódico?",
                            "Cómo va tu Jueves Jugoso?",
                            "Cómo va tu Viernes de Vino?",
                            "Qué tal el Sábado de Sofá?",
                            "Cómo te trata el Domingo Dulce?"
                        ]

                        print("Number of A lines:", num_A_lines)
                        if num_A_lines <= 2:
                            system_message_file = OPENER_FILE

                        elif 3 <= num_A_lines <= 6:
                            system_message_file = GETTING_TO_KNOW_FILE
                            #assistant_reply = find_and_replace_questions(assistant_reply, day_of_week, english_question_list, spanish_question_list)

                        else:
                            # Run a completion to determine "Yes" or "No"
                            with open("01-processing-files/01-split-sys-msg-method/03a-soft-close-detector-mid-sys-msg.txt", "r") as f:
                                temp_system_message = f.read().strip()

                            content = '{prompt}: \n "{text}"'.format(prompt=temp_system_message, text=formatted_text2)
                            messages = [{"role": "user", "content": content}]
                            response = openai.ChatCompletion.create(
                                model="gpt-3.5-turbo",
                                messages=messages
                            )
                            assistant_reply = response['choices'][0]['message']['content']

                            if assistant_reply == "No":
                                system_message_file = SOFT_CLOSE_MID_FILE
                            else:
                                system_message_file = HARD_CLOSE_FILE

                        # Read the selected system message
                        with open(system_message_file, "r") as f:
                            system_message = f.read().strip()

                        # Define the messages list with the {text} field
                        content = '{prompt}: \n "{text}"'.format(prompt=system_message, text=formatted_text2)
                        messages = [{"role": "user", "content": content}]

                        # Use openai.ChatCompletion.create() with the updated messages list
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=messages
                        )

                        assistant_reply = response['choices'][0]['message']['content']

                        # Modify assistant reply based on conditions
                        if system_message_file == GETTING_TO_KNOW_FILE:
                            if should_ask_question(formatted_text2):
                                assistant_reply = find_and_replace_questions(assistant_reply, day_of_week, english_question_list, spanish_question_list)

                        # Call emoji_reducer function to modify assistant_reply
                        assistant_reply = emoji_reducer(formatted_text2, assistant_reply)       
                        assistant_reply = assistant_reply.replace("!", "")
                        assistant_reply = assistant_reply.replace("¡", "")
                        assistant_reply = assistant_reply.replace("A:", "")
                        assistant_reply = assistant_reply.replace("A:", "¿")
                        #assistant_reply = assistant_reply.encode('latin1').decode('utf-8')
                        assistant_reply = assistant_reply.lower()
                        assistant_reply = assistant_reply.replace("\"", "")
                        assistant_reply = assistant_reply.split('\n')[0]




                        print("File used:", system_message_file)
                        print("Assistant reply:", assistant_reply)




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

                    else: 
                        print("She hasn't responded yet, so move on")
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
        
        
should_run = {'first_messages': True, 'conversations': True}



class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, str)
        self.widget.yview(tk.END)  # Scroll to the bottom
        self.widget.config(state=tk.DISABLED)


log_area = None  # Declare a global variable to hold the log area

def show_log_window():
    global log_area  # Use the global variable
    log_window = tk.Toplevel(app)
    log_window.title("3. Observe Logs")
    
    log_area = tk.Text(log_window, height=20, width=50)
    log_area.pack(padx=5, pady=5)
    log_area.config(state=tk.DISABLED)

    sys.stdout = TextRedirector(log_area)  # Redirect stdout to the Text widget




def start_execution(func_name):
    show_log_window()  # Show log window
    should_run[func_name] = True
    t = Thread(target=eval(f"execute_{func_name}"))
    t.start()
    if func_name == 'first_messages':
        print("Starting first_messages...") 
        update_status_label(left_frame, status_label_left, "Starting...")
    else:
        print("Starting conversations...")
        update_status_label(right_frame, status_label_right, "Starting...")

def stop_execution(func_name):
    should_run[func_name] = False
    if func_name == 'first_messages':
        
        update_status_label(left_frame, status_label_left, "Stopping...")
    else:
        update_status_label(right_frame, status_label_right, "Stopping...")



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
app = ThemedTk(theme="arc")  # Replace tk.Tk() with ThemedTk and specify the theme
app.title("AutoFlirt")

app.set_theme_advanced(
    theme_name='arc',  # Base theme
    hue=0.15,  # Change this value to shift the hue towards red
    brightness=1.0,  # Keep it at default
    saturation=1.0,  # Keep it at default
    preserve_transparency=True  # Preserves transparency
)


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
title_label = tk.Label(title_frame, text="AutoFlirt", font=("Arial", 32), background=bg_color, anchor="w", justify="left", foreground=dark_grey)
title_label.pack(side=tk.LEFT, fill="x")

# Toggle button
toggle_frame = tk.Frame(title_frame, bg=bg_color)
toggle_frame.pack(side=tk.RIGHT)

toggle_var = tk.IntVar(value=0)
style = ttk.Style()
style.configure('TCheckbutton', background=bg_color)

toggle_button = ttk.Checkbutton(toggle_frame, text="Active Mode", variable=toggle_var, style='TCheckbutton')
toggle_button.pack(side=tk.TOP)

# Toggle description
toggle_description = tk.Label(toggle_frame, text="Unchecked: Test mode - to ensure it's working\nChecked: Sends messages", wraplength=150, font=("Arial", 7), background=bg_color, anchor="e", justify="left", foreground=light_grey)
toggle_description.pack(side=tk.TOP, fill="x")

# Description
description_label = tk.Label(home_tab, text="Automate your Tinder experience! AutoFlirt sends flirty replies, sets up dates, and collects phone numbers for you.", wraplength=400, font=("Arial", 10), background=bg_color, anchor="w", justify="left", foreground=light_grey)
description_label.pack(fill="x", padx=20, pady=10)
###### 1. End Title and Description #########




####### 1a Line Breaker #######################

# Initialize a Canvas for the line break
line_break1a = tk.Canvas(home_tab, bg=bg_color, height=2, bd=0, highlightthickness=0)
line_break1a.pack(fill=tk.X, padx=5, pady=10)  # Add some padding around the line

def whiteraw_line(event):
    line_break1a.delete("all")  # Remove the old line
    line_break1a.create_line(10, 2, event.width - 10, 2, fill="#b8b7b6", width=3)  # Create a new line with padding

line_break1a.bind("<Configure>", whiteraw_line)


######### 1a. End Line Break        #########











######### 2. Preferences            #########

# Preferences Title and Divider 
preferences_title = tk.Label(home_tab, text="1. Preferences", font=("Arial", 16), bg=bg_color, foreground=dark_grey)
preferences_title.pack(anchor=tk.W, padx=20, pady=10)






# Create a Canvas with the background color
canvas = tk.Canvas(home_tab, bg=bg_color, highlightthickness=0, highlightbackground=bg_color, highlightcolor=bg_color, height=150)
canvas.pack(side=tk.TOP, padx=20, pady=10, fill=tk.BOTH)  # Changed padx to 20

# Create a Frame (tk.Frame) to add to the Canvas
preferences_frame = tk.Frame(canvas, bg=bg_color, bd=0)
canvas_frame = canvas.create_window((0, 0), window=preferences_frame, anchor=tk.NW)

# Configure column widths
preferences_frame.grid_columnconfigure(0, minsize=150)  # Set minimum column width to 150 pixels

# For debugging
#preferences_frame.config(bg='red')
#canvas.config(bg='green')


# Short Label for Days Threshold using tk.Label
days_label = tk.Label(preferences_frame, text="Days Limit: ", bg=bg_color, font=("Arial", 10), foreground=light_grey)
days_label.grid(row=0, column=0, sticky=tk.W, padx=(20, 0))  # Added tuple for padx

# Entry for Days Threshold
days_entry = ttk.Entry(preferences_frame, width=20)  # Specified width
days_entry.grid(row=0, column=2, sticky=tk.E)
days_entry.insert(0, "7")  # Default value

# Extra info under the "Days Limit" label
extra_info_label = tk.Label(preferences_frame, 
                            text="Set the maximum days since last message for replies. If the last message from someone exceeds this limit, the bot will not respond.",
                            bg=bg_color, 
                            font=("Arial", 8), 
                            wraplength=350,  # Adjust this value based on your layout
                            justify=tk.LEFT,
                            foreground=light_grey) # Text justification
extra_info_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=(20, 0), pady=(0, 10))  # Added pady


# Language Selection Label using tk.Label
language_label = tk.Label(preferences_frame, text="Select Language:", bg=bg_color, font=("Arial", 10), foreground=light_grey)
language_label.grid(row=2, column=0, sticky=tk.W, padx=(20, 0), pady=(10, 0))  # Added pady and changed row to 2


# Language Selection ComboBox
language_combo = ttk.Combobox(preferences_frame, values=["English", "Spanish"], width=18)  # Specified width to match Entry
language_combo.grid(row=2, column=2, sticky=tk.E, pady=(10, 0))  # Change row to 2
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
















op_title = tk.Label(home_tab, text="2. Select Operation", font=("Arial", 16), bg=bg_color, foreground=dark_grey)
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
left_title = tk.Label(left_frame, text="a. First Messages", bg=bg_color, font=("Arial", 13), justify="center", foreground=dark_grey)
left_title.pack(anchor=tk.W, pady=5)

# Setting wraplength for left_desc
left_desc = tk.Label(left_frame, text="Sends first messages to people you have matched with.", bg=bg_color, font=("Arial", 9), justify="left", foreground=light_grey, wraplength=190)
left_desc.pack(anchor=tk.W, pady=5)


status_label_left = tk.Label(left_frame, text="", bg=bg_color, font=("Arial", 9), foreground=light_grey)
status_label_right = tk.Label(right_frame, text="", bg=bg_color, font=("Arial", 9), foreground=light_grey)

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
right_title = tk.Label(right_frame, text="b. Respond to Messages", bg=bg_color, font=("Arial", 13), justify="center", foreground=dark_grey)
right_title.pack(anchor=tk.W, pady=5)

# Setting wraplength for right_desc
right_desc = tk.Label(right_frame, text="Replies to received messages using our custom-trained bot.", bg=bg_color, font=("Arial", 9), justify="left", foreground=light_grey, wraplength=190)
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


def get_text_between_tags(file_path, start_tag, end_tag=""):
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
    title1 = tk.Label(new_window, text="1. Customize profile", font=("Arial", 16), anchor="w", bg=bg_color)
    title1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Elements for Profile
    description_label1 = tk.Label(new_window, text="• Enter your profile in the text box below\n• The model will use this to personalise your conversartions\n• Talk in the second person e.g 'He is from Iceland' \n• Use the below numbered list as a guide \n\n1. Where you're from\n2. Age\n3. Past education/career info (short)\n4. Current job\n5. Hobbies\n6. Life Achievements\n7. Where you live now.", anchor="w", bg=bg_color, justify=tk.LEFT)  # Your text here
    description_label1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    text_entry1 = tk.Text(new_window, height=10, width=40, font=("Arial", 12))
    
    text_entry1.grid(row=2, column=0, padx=10, pady=10)
    text_entry1.insert(tk.END, profile_text)
    save_button1 = ttk.Button(new_window, text="Save Profile", command=lambda: save_profile(text_entry1, saved_label1, "# Profile of A:"))
    save_button1.grid(row=3, column=0)
    saved_label1 = tk.Label(new_window, text="", bg=bg_color)
    saved_label1.grid(row=4, column=0)
    
    # Title for Skills
    title2 = tk.Label(new_window, text="2. Customize your skills", font=("Arial", 16), anchor="w", bg=bg_color)
    title2.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    # Elements for Skills
    description_label2 = tk.Label(new_window, text="• Add your skills in Bullet point form \n• For example '* Great painter' is one bullet", anchor="w", bg=bg_color, justify=tk.LEFT)  # Your text here
    description_label2.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    text_entry2 = tk.Text(new_window, height=10, width=40, font=("Arial", 12))
    text_entry2.grid(row=2, column=2, padx=10, pady=10)
    text_entry2.insert(tk.END, skills_text)
    save_button2 = ttk.Button(new_window, text="Save Skills", command=lambda: save_profile(text_entry2, saved_label2, "# \"A\"'s skills:"))
    save_button2.grid(row=3, column=2)
    saved_label2 = tk.Label(new_window, text="", bg=bg_color)
    saved_label2.grid(row=4, column=2)

def show_cold_customisation__window():
    #bg_color = "#F0F0F0"
    new_window = tk.Toplevel()
    new_window.title("Customise Cold Openers")
    new_window.configure(bg=bg_color)

    # Title for Cold Openers
    title1 = tk.Label(new_window, text="1. Customize Cold Openers", font=("Arial", 16), anchor="w", bg=bg_color)
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


    
    text_entry1 = tk.Text(new_window, height=10, width=40, font=("Arial", 12))
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
    
    saved_label.config(text="Saved!")
         
        


customize_tab = tk.Frame(notebook, bg=bg_color)
notebook.add(customize_tab, text="Customize")
# Create a section frame within the customize_tab
section_frame = tk.Frame(customize_tab, bg=bg_color)
section_frame.grid(row=0, column=0)

# Add title
title_label = tk.Label(section_frame, text="1. Customize your profile", bg=bg_color, font=("Arial", 16), anchor="w", justify=tk.LEFT)
title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Add description
description_label = tk.Label(
    section_frame,
    text="This is where you can customize your profile so that the conversations are tailored to your personality and your lifestyle.",
    bg=bg_color,
    wraplength=400,
    font=("Arial", 10),
    anchor="w",
    justify=tk.LEFT
)
description_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)

# Add button
customise_button = ttk.Button(section_frame, text="Customize", command=show_customisation_window)
customise_button.grid(row=2, column=0)

# Add horizontal line break
line_break1a = tk.Canvas(section_frame, bg=bg_color, height=2, bd=0, highlightthickness=0)
line_break1a.grid(row=3, column=0, sticky="ew", padx=5, pady=10)

# Add second title
title_label2 = tk.Label(section_frame, text="2. Customize cold openers", bg=bg_color, font=("Arial", 16), anchor="w", justify=tk.LEFT)
title_label2.grid(row=4, column=0, padx=10, pady=10, sticky="w")

# Add second description
description_label2 = tk.Label(
    section_frame,
    text="This is where you can customize cold openers for initiating conversations.",
    bg=bg_color,
    wraplength=400,
    font=("Arial", 10),
    anchor="w",
    justify=tk.LEFT
)
description_label2.grid(row=5, column=0, sticky="w", padx=10, pady=10)

# Add second button
customise_openers_button = ttk.Button(section_frame, text="Customise Openers", command=show_cold_customisation__window)
customise_openers_button.grid(row=6, column=0)




#########


#app.geometry("800x600")
app.resizable(True, True)



app.mainloop()