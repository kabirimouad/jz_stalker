from dotenv import load_dotenv
import os
import time
import json
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

load_dotenv()
AUI_ID = os.getenv('AUI_ID')
PASSWORD = os.getenv('PASSWORD')
WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH')


def login(driver, EMAIL, PASSWORD):
    driver.get("https://my.aui.ma/ICS/")
    driver.set_window_size(1552, 832)
    driver.find_element(By.ID, "userName").click()
    driver.find_element(By.ID, "userName").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "siteNavBar_btnLogin").click()

def search_for_course(driver, course_code):
    # 1 | click | linkText=Students | 
    # driver.find_element(By.LINK_TEXT, "Students").click()
    driver.get("https://my.aui.ma/ICS/Students/")
    # 2 | click | id=pg1_V_lblAdvancedSearch | 
    driver.find_element(By.ID, "pg1_V_lblAdvancedSearch").click()
    # 3 | click | id=pg0_V_ddlTerm | 
    driver.find_element(By.ID, "pg0_V_ddlTerm").click()
    # 4 | select | id=pg0_V_ddlTerm | label=2022-2023 Academic Year - Spring Semester
    dropdown = driver.find_element(By.ID, "pg0_V_ddlTerm")
    dropdown.find_element(By.XPATH, "//option[. = '2023-2024 Academic Year - Fall Semester']").click()
    # 5 | click | id=pg0_V_txtCourseRestrictor | 
    driver.find_element(By.ID, "pg0_V_txtCourseRestrictor").click()

    # clear the input field (JZC stores the last search and it will cause a problem)
    driver.find_element(By.ID, "pg0_V_txtCourseRestrictor").clear()

    # 6 | type | id=pg0_V_txtCourseRestrictor | CSC 3351
    driver.find_element(By.ID, "pg0_V_txtCourseRestrictor").send_keys(course_code)
    # 7 | click | id=pg0_V_btnSearch | 
    driver.find_element(By.ID, "pg0_V_btnSearch").click()

def extract_table(driver):
    course_rows = []

    # Find the tbody element that contains the rows of the table
    tbody = driver.find_element(By.CSS_SELECTOR, 'tbody.gbody')

    # Find all of the rows in the table
    rows = tbody.find_elements(By.TAG_NAME, 'tr')

    # Loop through the rows
    for row in rows:
        # Find the cells in the row
        cells = row.find_elements(By.TAG_NAME, 'td')

        # rows that contain 11 cells are the ones we want
        if len(cells) != 11:
            continue

        # Extract the information from the cells
        course_code = cells[2].text
        course_name = cells[3].text
        professor = cells[4].text
        seats_open = cells[5].text

        course_rows.append({
            'course_code': course_code,
            'course_name': course_name,
            'professor': professor,
            'seats_open': seats_open
        })
        
        # Print the information
        print(f'Course code: {course_code} | Course name: {course_name} | Professor: {professor} | Seats open: {seats_open}')

    print("Done Extracting...")
    return course_rows


def get_course_code_from_user() -> str: 
    print("1. Track a course.\n2. Track a section.")
    choice: int = int(input("Hello Again! can you please specify which type of tracking you would like to perform(Choose a number): "))
    code: str = str(input("Type the course code: "))
    if choice == 1:
        return code
    elif choice == 2:
        section: int = int(input("Type the section: "))
        if int(section / 10) == 0: 
            return f'{code} 0{section}'
        else:
            return f'{code} {section}'
    else:
        print("Please, next time select from the choices we offered!")






if __name__ == '__main__':
    course_codes = {} 

    driver = webdriver.Chrome(WEBDRIVER_PATH)

    login(driver, AUI_ID, PASSWORD)
    print("Logged in successfully")
    
    try:
        course_code = get_course_code_from_user()
        print("Searching for course")
        search_for_course(driver, course_code)
    except:
        print("Error searching for course")
        driver.close()
        exit()

    try:
        print("Extracting table")
        course_rows = extract_table(driver)
    except:
        print("Error extracting table")
        driver.close()
        exit()


    # append to the dictionary of courses
    course_codes[course_code] = course_rows

    # write the dictionary to a json file
    with open('courses.json', 'w') as f:
        json.dump(course_codes, f, indent=4)

    driver.close()
