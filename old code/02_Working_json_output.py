#run:  DegreePathwayWebParser-env\Scripts\activate
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

JSON_FILES_FOLDER_PATH = 'T:\WalnutShrimp\py - Degree Pathway Web Parser\JSON Files'
JSON_DATA_FILE_PATH = JSON_FILES_FOLDER_PATH + "\\" +"data.json"

UML_CATALOG_URL = "https://www.uml.edu/catalog" # combine with another text to sight value
URL = 'https://www.uml.edu/catalog/undergraduate/engineering/departments/electrical-computer-engineering/degree-pathways/dp-ece-eecs-2023.aspx'

driver = webdriver.Firefox()
driver.get(url=URL)


classes_queue = []
temp_semester = []
academic_year_counter = 0
academic_year_key_counter = 0
academic_year_key = ['Freshman year', 'Sophomore year', 'Junior year', 'Senior year']
classes_key = ["Class Name", "Class ID", "Class Link", "Credit(s)"]
semester_counter = 1
col_text_counter = 0
tables = driver.find_elements(By.TAG_NAME,'table')

pathway = list()

full_academic_year = dict()
temp_academic_year = list()

for index, table in enumerate(tables, start=1):
    semester = dict()
    classes_list = []
    if semester_counter % 2 == 1:
        print("Fall Semester: ")
        semester["Semester"] = "Fall Semester"
    else: 
        print("Spring Semester: ")
        semester["Semester"] = "Spring Semester"
    semester_counter+=1
    
    rows = table.find_elements(By.TAG_NAME,'tr')    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME,'td')  
        col_text_counter = 0 
        class_container = dict()
                
        temp_class_ID = ''
        temp_class_LINK = ''
        
        for cell in cells:
            if (cell.text == "Total") or ((cell.text.isdigit()) and (int(cell.text) >= 8)):
                print("")
            else:
                if cell.find_elements(By.TAG_NAME, "a"):                    #get href link
                    a = cell.find_elements(By.TAG_NAME, "a")
                    for x in a:
                        print(x.text + f"!{col_text_counter}!", end=" ")
                        print(x.get_attribute("href"), end="\n")
                        temp_class_ID = x.text
                        temp_class_LINK = x.get_attribute("href")
                        
                else:
                    if (col_text_counter == 1):
                        class_container[classes_key[0]] = cell.text
                    if (col_text_counter == 2):
                        class_container[classes_key[1]] = (temp_class_ID)
                        class_container[classes_key[2]] = (temp_class_LINK)
                        class_container[classes_key[3]] = (cell.text)
                        classes_list.append(class_container)
                        print(cell.text + f"!{col_text_counter}!" , end=' ')
                    if (cell.text.isdigit()):
                        print("\n")
            col_text_counter +=1
        class_container = dict()
    semester["classes"] = classes_list
    temp_academic_year.append(semester)
    classes_list = []
    print("------------\n------------")  
with open(JSON_DATA_FILE_PATH, "w") as w_file:
    json.dump(temp_academic_year, w_file, indent= 4)


driver.close()    
#end