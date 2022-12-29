from stalk import *
import random

course_codes = []
courses = {}

while True:
    course = input("Enter course code (or 'done' to stop): ")
    if course.lower() == 'done':
        break
    else:
        course_codes.append(course)

load_dotenv()
AUI_ID = os.getenv('AUI_ID')
PASSWORD = os.getenv('PASSWORD')
WEBDRIVER_PATH = os.getenv('WEBDRIVER_PATH')
driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH)



login(driver, AUI_ID, PASSWORD)
print("Logged in successfully")

while True:

    for course_code in course_codes:
        try:
            print("Searching for course")
            search_for_course(driver, course_code)
        except:
            print("Error searching for course")
            continue

        try:
            print("Extracting table")
            course_rows = extract_table(driver)
        except:
            print("Error extracting table")
            continue

        # append to the dictionary of courses
        courses[course_code] = course_rows

    driver.close()

    # open the old courses file and compare it to the new one
    changed = False # if changed is true, then we need to store the new version
    old_courses_exist = True

    try:
        with open('courses.json', 'r') as f:
            old_courses = json.load(f)
    except FileNotFoundError:
        old_courses_exist = False

    if old_courses_exist:
        for key in courses:
            if key in old_courses:
                if len(courses[key]) != len(old_courses[key]):
                    print(f"Number of section for {key} has changed, new number of sections is {len(courses[key])}")
                    changed = True
                    # Check the common sections
                    for i in range(min(len(courses[key]), len(old_courses[key]))):
                        if courses[key][i]['professor'] != old_courses[key][i]['professor']:
                            print(f"Field {courses[key][i]['course_code']} has changed: professor. Old professor : {old_courses[key][i]['professor']} New professor :{courses[key][i]['professor']}")
                            changed = True
                        if courses[key][i]['seats_open'] != old_courses[key][i]['seats_open']:
                            print(f"Field {courses[key][i]['course_code']} has changed: seats_open. Previous : {old_courses[key][i]['seats_open']} New : {courses[key][i]['seats_open']}")
                            changed = True
                else:
                    # The number of sections is the same, so we can just iterate through all of them
                    for i in range(len(courses[key])):
                        if courses[key][i]['professor'] != old_courses[key][i]['professor']:
                            print(f"Field {courses[key][i]['course_code']} has changed: professor. Old professor : {old_courses[key][i]['professor']} New professor :{courses[key][i]['professor']}")
                            changed = True
                        if courses[key][i]['seats_open'] != old_courses[key][i]['seats_open']:
                            print(f"Field {courses[key][i]['course_code']} has changed: seats_open. Previous : {old_courses[key][i]['seats_open']} New : {courses[key][i]['seats_open']}")
                            changed = True


    if changed or not old_courses_exist:
        with open('courses.json', 'w') as f:
            json.dump(courses, f, indent=4)
    
    # wait an interval between 3 and 5 minutes
    time.sleep(random.randint(180, 300))

