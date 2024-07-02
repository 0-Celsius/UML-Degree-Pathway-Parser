import json

from selenium import webdriver
from selenium.webdriver.common.by import By


def create_JSON_file():
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

    full_year = False
    full_year_counter = 0

    semester_counter = 1
    col_text_counter = 0
    full_academic_year = list()

    tables = driver.find_elements(By.TAG_NAME,'table')
    for table in tables:
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
                            class_container[CLASSES_KEY[0]] = cell.text
                        if (col_text_counter == 2):
                            class_container[CLASSES_KEY[1]] = (temp_class_ID)
                            class_container[CLASSES_KEY[2]] = (temp_class_LINK)
                            class_container[CLASSES_KEY[3]] = (cell.text)
                            classes_list.append(class_container)
                        if (cell.text.isdigit()):
                            pass
                col_text_counter +=1
            class_container = dict()
        semester["classes"] = classes_list
        full_academic_year.append(semester)
        classes_list = []
        if(full_year == True):
            pathway[ACADEMIC_YEAR_KEY[full_year_counter]] = full_academic_year
            full_academic_year = list()
            full_year_counter += 1
            full_year = False
            
    with open(JSON_DATA_FILE_PATH, "w") as w_file:
        json.dump(pathway, w_file, indent= 4)

    print("done creating your pathway JSON file!")        
    driver.close()    
