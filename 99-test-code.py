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
import re  # Make sure to import the regular expression library

# Step 1: Read the file into a single string
with open("personal_details.txt", "r") as f:
    content = f.read()

# Step 2: Use a regular expression to find the phone number
phone_number = None
match = re.search(r'Your phone number:\s*([\+\d]+)', content)
if match:
    phone_number = match.group(1).strip()  # Get the first capturing group and strip whitespace

print("Phone number from file is: ", phone_number if phone_number else "Not found")
