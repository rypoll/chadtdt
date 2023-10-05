import pandas as pd
import random
import re
from datetime import datetime




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
                    continue

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