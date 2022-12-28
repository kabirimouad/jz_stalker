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


driver_path = r"C:\chromedriver.exe" 


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
    driver.find_element(By.LINK_TEXT, "Students").click()
    # 2 | click | id=pg1_V_lblAdvancedSearch | 
    driver.find_element(By.ID, "pg1_V_lblAdvancedSearch").click()
    # 3 | click | id=pg0_V_ddlTerm | 
    driver.find_element(By.ID, "pg0_V_ddlTerm").click()
    # 4 | select | id=pg0_V_ddlTerm | label=2022-2023 Academic Year - Spring Semester
    dropdown = driver.find_element(By.ID, "pg0_V_ddlTerm")
    dropdown.find_element(By.XPATH, "//option[. = '2022-2023 Academic Year - Spring Semester']").click()
    # 5 | click | id=pg0_V_txtCourseRestrictor | 
    driver.find_element(By.ID, "pg0_V_txtCourseRestrictor").click()
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
        professor = cells[4].text
        seats_open = cells[5].text

        course_rows.append({
            'course_code': course_code,
            'professor': professor,
            'seats_open': seats_open
        })
        
        # Print the information
        print(f'Course code: {course_code} | Professor: {professor} | Seats open: {seats_open}')

    print("Done Extracting...")
    return course_rows



if __name__ == '__main__':
    courses = {} 
    course_code = "CSC 3326"

    driver = webdriver.Chrome(WEBDRIVER_PATH)

    login(driver, AUI_ID, PASSWORD)
    print("Logged in successfully")

    try:
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
    courses[course_code] = course_rows

    # write the dictionary to a json file
    with open('courses.json', 'w') as f:
        json.dump(courses, f, indent=4)

    driver.close()
