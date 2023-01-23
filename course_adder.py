from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def course_adder(course_code, driver):
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.ID, "pg0_V_divMain")))

    # find the row containing the course code you're looking for
    course_checkbox = table.find_element(By.XPATH, f"//input[@title='Add {course_code}']")
    course_checkbox.click()


    # # find the checkbox for that course and click it
    # checkbox = course_row.find_element_by_xpath(".//input[@type='checkbox']")
    # checkbox.click()

    # find the 'Add Courses' button and click it
    add_button = driver.find_element(By.ID, "pg0_V_btnAddCourse")
    add_button.click()
