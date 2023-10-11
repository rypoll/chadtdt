import pandas as pd
import random
import re
from datetime import datetime
import os




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