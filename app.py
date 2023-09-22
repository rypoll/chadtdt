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
from helper_functions import detect_phone_number, contains_emoji, emoji_reducer, should_ask_question, find_and_replace_questions, count_A_lines
import tkinter as tk
from tkinter import ttk
from threading import Thread
import sv_ttk
from ttkthemes import ThemedTk 

chromedriver_path = r'04-assets\\chromedriver.exe'
extension_path2 = r'04-assets\\uBlock-Origin.crx'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension(extension_path2)
chrome_options.add_argument('--start-maximized') 



class RedirectStdout:
    def __init__(self, widget):
        self.widget = widget

    def write(self, s):
        self.widget.insert(tk.END, s)
        self.widget.see(tk.END)

    def flush(self):
        pass  # Add a flush method to avoid the error

# Long-running functions
should_run = {'first_messages': True, 'conversations': True}

def execute_first_messages():
    while should_run['first_messages']:
        try:
            print("Executing first messages...")
            

            profile_folder_name = 'profiles'

            # Your profile directory path
            profile_directory = os.path.join(os.getcwd(), profile_folder_name)

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
            chrome_options.add_argument(f"user-data-dir={profile_directory}")

            try:
                driver.quit()
            except:
                pass


            driver = webdriver.Chrome(options=chrome_options)
            time.sleep(random.uniform(3, 6))
            # Open the website
            driver.get('https://www.tinder.com/')

            # If it's the first time or the directory was empty, ask the user to log in manually
            if first_time or is_empty:
                input("Press Enter after you have logged in manually...")

            print("Waiting for user to log in.")
            #time.sleep(60)  # 60 seconds, change it to the time you need

            print("Waiting for 'Matches' button to appear.")
            if is_empty == True:
                wait = WebDriverWait(driver, 60)
            else:
                wait = WebDriverWait(driver, 10)
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
                print(f"Loop iteration {i+1}")
                
                ###############################  START 2. Click First Match

                print("Locating the third 'li' in the first 'ul'.")
                third_li = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//ul)[1]/li[{first_match}]")))

                try:
                    print("Clicking the third 'li'.")
                    third_li.click()
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
                with open('messages/01-cold-openers-es.txt', 'r') as file:
                    lines = file.readlines()

                # Remove any leading/trailing whitespace from each line
                lines = [line.strip() for line in lines]

                # Randomly pick a line from the list
                random_line = random.choice(lines)

                # Assuming 'driver' is your initialized WebDriver instance
                actions = ActionChains(driver)
                actions.send_keys(random_line).perform()
                print(f"Send message {random_line}")
                time.sleep(random.uniform(3, 6))
                actions.send_keys(Keys.RETURN)  # Sending the Enter key

                actions.perform()  # Perform the action
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
    while should_run['conversations']:
        try:
            print("Executing conversations...")
            
        

            profile_folder_name = 'profiles'

            # Your profile directory path
            profile_directory = os.path.join(os.getcwd(), profile_folder_name)

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
                    driver = webdriver.Chrome(options=chrome_options)
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
            if first_time or is_empty:
                input("Press Enter after you have logged in manually...")

            print("Waiting for user to log in.")
            #time.sleep(60)  # 60 seconds, change it to the time you need

            print("Waiting for 'Messages' button to appear.")
            if is_empty == True:
                wait = WebDriverWait(driver, 60)
            else:
                wait = WebDriverWait(driver, 10)
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
                            actions.send_keys(assistant_reply).perform()
                            print(f"Send message {assistant_reply}")
                            #time.sleep(random.uniform(20, 40))
                            actions.send_keys(Keys.RETURN)  # Sending the Enter key

                            actions.perform()  # Perform the action
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
        
        
def start_execution(func_name):
    should_run[func_name] = True
    t = Thread(target=eval(f"execute_{func_name}"))
    t.start()

def stop_execution(func_name):
    should_run[func_name] = False


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
app.title("ChadTDT - The Date Texter")

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



###### 1. Title and description #############



# Then use this color for your labels
# Left-align the title
title_label = tk.Label(app, text="AutoFlirt", font=("Arial", 32), background=bg_color, anchor="w", justify="left", foreground=dark_grey)
title_label.pack(fill="x", padx=20, pady=10)  # Fill the available horizontal space and pad 20 pixels on each side

# Left-align the description
description_label = tk.Label(app, text="Automate your Tinder experience! AutoFlirt sends flirty replies, sets up dates, and collects phone numbers for you.", wraplength=400, font=("Arial", 10), background=bg_color, anchor="w", justify="left", foreground=light_grey)
description_label.pack(fill="x", padx=20, pady=10)  # Fill the available horizontal space and pad 20 pixels on each side





###### 1. End Title and Description #########



####### 1a Line Breaker #######################

# Initialize a Canvas for the line break
line_break1a = tk.Canvas(app, bg=bg_color, height=2, bd=0, highlightthickness=0)
line_break1a.pack(fill=tk.X, padx=5, pady=10)  # Add some padding around the line

def whiteraw_line(event):
    line_break1a.delete("all")  # Remove the old line
    line_break1a.create_line(10, 2, event.width - 10, 2, fill="#b8b7b6", width=3)  # Create a new line with padding

line_break1a.bind("<Configure>", whiteraw_line)


######### 1a. End Line Break        #########











######### 2. Preferences            #########

# Preferences Title and Divider 
preferences_title = tk.Label(app, text="1. Preferences", font=("Arial", 16), bg=bg_color, foreground=dark_grey)
preferences_title.pack(anchor=tk.W, padx=20, pady=10)






# Create a Canvas with the background color
canvas = tk.Canvas(app, bg=bg_color, highlightthickness=0, highlightbackground=bg_color, highlightcolor=bg_color, height=150)
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
line_break2a = tk.Canvas(app, bg=bg_color, height=2, bd=0, highlightthickness=0)
line_break2a.pack(fill=tk.X, padx=5, pady=10)  # Add some padding around the line

def whiteraw_line(event):
    line_break2a.delete("all")  # Remove the old line
    line_break2a.create_line(10, 2, event.width - 10, 2, fill="#dee0df", width=3)  # Create a new line with padding

line_break2a.bind("<Configure>", whiteraw_line)


######### 2a. End Line Break        #########

















######### 3. START Operations New Section #########

# Preferences Title and Divider 
preferences_title = tk.Label(app, text="2. Select Operation", font=("Arial", 16), bg=bg_color, foreground=dark_grey)
preferences_title.pack(anchor=tk.W, padx=20, pady=10)



def update_vert_line(event):
    # Update the vertical line to match the new height of the new_section_frame
    vert_line_break.coords(line, 2, 0, 2, event.height)

# Create a new Frame for the new section
new_section_frame = tk.Frame(app, bg=bg_color)
new_section_frame.pack(side=tk.TOP, padx=20, pady=10, fill=tk.X)

new_section_frame.bind("<Configure>", update_vert_line)

# Create left child frame
left_frame = tk.Frame(new_section_frame, bg=bg_color, width=200)
left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)

# Vertical Line Breaker
vert_line_break = tk.Canvas(new_section_frame, bg=bg_color, width=2, bd=0, highlightthickness=0)
vert_line_break.pack(side=tk.LEFT, fill=tk.Y, padx=10)  # Add some padding around the line
line = vert_line_break.create_line(2, 0, 2, 100, fill="#dee0df", width=3)  # Create a new line with padding

# Create right child frame
right_frame = tk.Frame(new_section_frame, bg=bg_color, width=200)
right_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

# Title and description on the left side
left_title = tk.Label(left_frame, text="A. First Messages", bg=bg_color, font=("Arial", 13), justify="center", foreground=dark_grey)
left_title.pack(anchor=tk.W, pady=5)

left_desc = tk.Label(left_frame, text="Description for First Messages.", bg=bg_color, font=("Arial", 9), justify="center", foreground=light_grey)
left_desc.pack(anchor=tk.W, pady=5)






# Title and description on the right side
right_title = tk.Label(right_frame, text="B. Respond to Messages", bg=bg_color, font=("Arial", 13), justify="center", foreground=dark_grey)
right_title.pack(anchor=tk.W, pady=5)

right_desc = tk.Label(right_frame, text="Description for Respond to Messages.", bg=bg_color, font=("Arial", 9), justify="center", foreground=light_grey)
right_desc.pack(anchor=tk.W, pady=5)

######### 3. End New Section #########

####### 3a Line Breaker #######################

# Initialize a Canvas for the line break
line_break3a = tk.Canvas(app, bg=bg_color, height=2, bd=0, highlightthickness=0)
line_break3a.pack(fill=tk.X, padx=5, pady=10)  # Add some padding around the line

def line3a_draw(event):
    line_break3a.delete("all")  # Remove the old line
    line_break3a.create_line(10, 2, event.width - 10, 2, fill="#dee0df", width=3)  # Create a new line with padding

line_break3a.bind("<Configure>", line3a_draw)

######### 3a. End Line Break #########


app.mainloop()