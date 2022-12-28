from dotenv import load_dotenv
import os
import time
import json
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 

driver_path = r"C:\chromedriver.exe" 


load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH')

driver = webdriver.Chrome(WEBDRIVER_PATH)
