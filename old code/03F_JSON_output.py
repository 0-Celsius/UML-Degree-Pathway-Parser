#run:  DegreePathwayWebParser-env\Scripts\activate
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

JSON_FILES_FOLDER_PATH = 'T:\WalnutShrimp\py - Degree Pathway Web Parser\JSON Files'
JSON_DATA_FILE_PATH = JSON_FILES_FOLDER_PATH + "\\" +"data.json"

URL = 'https://www.uml.edu/catalog/undergraduate/engineering/departments/electrical-computer-engineering/degree-pathways/dp-ece-eecs-2023.aspx'

'''
UNDERGRADUATE_URL= "https://www.uml.edu/catalog/undergraduate"
URL = input("please input an undergraduate degree pathway to parse: ")
while(UNDERGRADUATE_URL not in URL):
    URL = input("please input an undergraduate degree pathway to parse: ")
'''    
driver = webdriver.Firefox()
driver.get(url=URL)

pathway = dict()

academic_year_key = ['Freshman year', 'Sophomore year', 'Junior year', 'Senior year']
classes_key = ["Class Name", "Class ID", "Class Link", "Credit(s)"]

full_year = False
full_year_counter = 0

semester_counter = 1
col_text_counter = 0
full_academic_year = list()

tables = driver.find_elements(By.TAG_NAME,'table')
for index, table in enumerate(tables, start=1):
    semester = dict()
    classes_list = []
    if semester_counter % 2 == 1:
        semester["Semester"] = "Fall Semester"
    else: 
        semester["Semester"] = "Spring Semester"
        full_year = True
    semester_counter+=1
    
    rows = table.find_elements(By.TAG_NAME,'tr')    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME,'td')  
        col_text_counter = 0 
        class_container = dict()
                
        temp_class_ID = list()
        temp_class_LINK = list()
        
        for cell in cells:
            if (cell.text == "Total") or ((cell.text.isdigit()) and (int(cell.text) >= 8)):
                pass
            else:
                if cell.find_elements(By.TAG_NAME, "a"):                    
                    a = cell.find_elements(By.TAG_NAME, "a")
                    for x in a:
                        temp_class_ID.append(x.text)
                        temp_class_LINK.append(x.get_attribute("href"))                        
                else:
                    if (col_text_counter == 1):
                        class_container[classes_key[0]] = cell.text
                    if (col_text_counter == 2):
                        class_container[classes_key[1]] = (temp_class_ID)
                        class_container[classes_key[2]] = (temp_class_LINK)
                        class_container[classes_key[3]] = (cell.text)
                        classes_list.append(class_container)
                    if (cell.text.isdigit()):
                        pass
            col_text_counter +=1
        class_container = dict()
    semester["classes"] = classes_list
    full_academic_year.append(semester)
    classes_list = []
    if(full_year == True):
        pathway[academic_year_key[full_year_counter]] = full_academic_year
        full_academic_year = list()
        full_year_counter += 1
        full_year = False
        
with open(JSON_DATA_FILE_PATH, "w") as w_file:
    json.dump(pathway, w_file, indent= 4)

print("Done")        
driver.close()    



#end