#run:  DegreePathwayWebParser-env\Scripts\activate
# saved on 12/31/2023
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

class semester():
    def __init__(self, quarter, course_ID, course_name, link, credit):
        self.quarter = quarter
        self.course_ID = course_ID
        self.course_name = course_name
        self.link = link
        self.credit = credit
        



def get_academic_years():
    academic_years = []
    h2 = driver.find_elements(By.TAG_NAME, 'h2')
    for x in h2: 
        if (x.text.__contains__('YEAR')): 
            academic_years.append(x.text)
    #print(academic_years)                  # DEBUG
    return academic_years




classes_queue = []
temp_semester = []
semester_counter = 1
col_text_counter = 0
tables = driver.find_elements(By.TAG_NAME,'table')

for index, table in enumerate(tables, start=1):
    #print(f"Table {index}:")    
    if semester_counter % 2 == 1:
        print("Fall Semester: ")
    else: 
        print("Spring Semester: ")
    semester_counter+=1
    rows = table.find_elements(By.TAG_NAME,'tr')    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME,'td')  
        col_text_counter = 0 
        for cell in cells:
            if (cell.text == "Total") or ((cell.text.isdigit()) and (int(cell.text) >= 8)):
                print("")
            else:
                if cell.find_elements(By.TAG_NAME, "a"):                    #get href link
                    a = cell.find_elements(By.TAG_NAME, "a")
                    for x in a:
                        print(x.text + f"!{col_text_counter}!", end=" ")
                        print(x.get_attribute("href"), end="\n")
                else:
                    print(cell.text + f"!{col_text_counter}!" , end=' ')
                    if (cell.text.isdigit()):
                        print("\n")
                col_text_counter +=1
    print("------------\n------------")  
    
    
'''
tables = driver.find_elements(By.TAG_NAME,'table')
rows = tables[0].find_elements(By.TAG_NAME,'tr')    
print(type(rows))
def a():
    for row in rows:
        cells = row.find_elements(By.TAG_NAME,'td')  
        for cell in cells:
            print(cell.text)  
    print("\n")  

'''


def main():
    academic_years = get_academic_years()
    print(academic_years)
    
    
    '''
    academic_year   >>  Fall        >>  Class[] 
                            
                    >>  Spring      >>  Class[]
    
    
    '''




#main()
driver.close()    
#end