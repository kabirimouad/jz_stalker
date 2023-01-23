from stalk import *
from mailer import *
import random
import logging
from course_adder import course_adder as add_course 
import argparse 

# parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--add', action= 'store_true', help='Add courses to the cart')
args = parser.parse_args()
add_course_flag = args.add


outlook_email = os.getenv('OUTLOOK_EMAIL')
outlook_password = os.getenv('OUTLOOK_PASSWORD')


course_codes = [] # list of course codes to track
courses = {} # dictionary of courses, where the key is the course code and the value is a list of dictionaries, each dictionary representing a section

# create a logger to log the output of the program
logger = logging.getLogger('stalk')
# set the log level
logger.setLevel(logging.INFO)
# create a file handler to write the log messages to a file
file_handler = logging.FileHandler('app.log')
# create a formatter to specify the format of the log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# set the formatter for the file handler
file_handler.setFormatter(formatter)
# add the file handler to the logger
logger.addHandler(file_handler)
logger.info('Script started')


while True:
    course = input("Enter course code (or 'done' to stop): ")
    if course.lower() == 'done':
        break
    # check if the course code is valid
    elif len(course) != 8 and len(course) != 11:
        print("Invalid course code")
    else:
        course_codes.append(course)

# put course_codes in a file
# this is helpful if we want to run the program in the background and add courses to track to a file
with open('course_codes.txt', 'w') as f:
    for course in course_codes:
        f.write(course + '\n')

load_dotenv()
AUI_ID = os.getenv('AUI_ID')
PASSWORD = os.getenv('PASSWORD')
WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH')

# to remove unnecessary logs from the console
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, executable_path=WEBDRIVER_PATH)

login(driver, AUI_ID, PASSWORD)
print("Logged in successfully")

while True:
    email_message = "" # message to send in the email

    # open the file and get the course codes appended to it
    with open('course_codes.txt', 'r') as f:
        course_codes = []
        for line in f:
            course_codes.append(line.strip())

    

    for course_code in course_codes:
        try:
            print("Searching for course")
            search_for_course(driver, course_code)
        except:
            print("Error searching for course")
            message = "Error searching for course " + course_code
            email_message += message + "\n"
            logger.error(f"Error searching for course {course_code}")
            continue

        try:
            print("Extracting table")
            course_rows = extract_table(driver)
        except:
            print("Error extracting table")
            logger.error(f"Error extracting table for course {course_code}")
            continue

        # append to the dictionary of courses
        courses[course_code] = course_rows


    # open the old courses file and compare it to the new one
    changed = False # if changed is true, then we need to store the new version
    old_courses_exist = True

    try:
        with open('courses.json', 'r') as f:
            old_courses = json.load(f)
    except FileNotFoundError:
        old_courses_exist = False
    
    print("Checking for changes...")

    if old_courses_exist:
        for key in courses:
            if key in old_courses:
                if len(courses[key]) != len(old_courses[key]):
                    message = f"- Number of sections for {key} ({old_courses[key][0]['course_name']}) has changed. Old : {len(old_courses[key])} New : {len(courses[key])}"
                    email_message += message + "\n"
                    print(message)
                    logger.info(message) 
                    changed = True
                    # Check the common sections
                    for i in range(min(len(courses[key]), len(old_courses[key]))):
                        if courses[key][i]['professor'] != old_courses[key][i]['professor']:
                            message = f"- Field {courses[key][i]['course_code']} ({courses[key][i]['course_name']}) has changed: \"professor\". Old professor : {old_courses[key][i]['professor']} New professor : {courses[key][i]['professor']}"
                            email_message += message + "\n"
                            print(message)
                            logger.info(message)
                            changed = True
                        if courses[key][i]['seats_open'] != old_courses[key][i]['seats_open']:
                            message = f"- Field {courses[key][i]['course_code']} ({courses[key][i]['course_name']}) has changed: \"seats_open\". Previous : {old_courses[key][i]['seats_open']} New : {courses[key][i]['seats_open']}"
                            email_message += message + "\n"
                            print(message)
                            logger.info(message)
                            changed = True
                else:
                    # The number of sections is the same, so we can just iterate through all of them
                    for i in range(len(courses[key])):
                        if courses[key][i]['professor'] != old_courses[key][i]['professor']:
                            message = f"- Field {courses[key][i]['course_code']} ({courses[key][i]['course_name']}) has changed: \"professor\". Old professor : {old_courses[key][i]['professor']} New professor :{courses[key][i]['professor']}"
                            email_message += message + "\n"
                            print(message)
                            logger.info(message)
                            changed = True
                        if courses[key][i]['seats_open'] != old_courses[key][i]['seats_open']:
                            message = f"- Field {courses[key][i]['course_code']} ({courses[key][i]['course_name']}) has changed: \"seats_open\". Previous : {old_courses[key][i]['seats_open']} New : {courses[key][i]['seats_open']}"
                            email_message += message + "\n"
                            print(message)
                            logger.info(message)
                            changed = True

                            # if the number of seats open is greater than 0, then we need to add the course if the flag is set
                        
                        seats_open = courses[key][i]['seats_open'].split('/')[0]
                        if int(seats_open) > 0 and add_course_flag:
                            logger.info(f"Adding course {courses[key][i]['course_code']}")
                            add_course(courses[key][i]['course_code'], driver) 
            else:
                message = f"- New course {key} has been added"
                print(message)
                logger.info(message)
                changed = True

    print("Done checking for changes")

    if changed or not old_courses_exist:
        with open('courses.json', 'w') as f:
            json.dump(courses, f, indent=4)
        # send an email
        if email_message != "":
            try :
                print("Sending email")
                send_email(outlook_email, outlook_password, "Jz_Stalker Update!", email_message)
                logger.info("Email sent")
            except:
                print("Error sending email")
                logger.error("Error sending email")
            email_message = ""

    

    
    # wait an interval between 3 and 5 minutes
    print("Waiting for next check...")
    time.sleep(random.randint(0, 30))


# driver.close()