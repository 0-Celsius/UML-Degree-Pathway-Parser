#run:  DegreePathwayWebParser-env\Scripts\activate
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidArgumentException

ACADEMIC_YEAR_KEY = ['Freshman year', 'Sophomore year', 'Junior year', 'Senior year']
CLASSES_KEY = ["Class Name", "Class ID", "Class Link", "Credit(s)"]

JSON_FILES_FOLDER_PATH = os.path.join(os.getcwd(), 'JSON Files')
LOG_FILES_FOLDER_PATH = os.path.join(os.getcwd(), 'Log Files')

JSON_DATA_FILE_PATH = JSON_FILES_FOLDER_PATH + "\\" +"data.json"
LOG_DATA_FILE_PATH = LOG_FILES_FOLDER_PATH + "\\" +"log.txt"



class class_container:
    def __init__(self, name, ID, link, credits): 
        self.name = name
        self.ID = ID
        self.link = link
        self.credits = credits
        

def print_JSON_file_data(JSON_file, keyword):
    with open(JSON_file, "r") as file:
        data = json.load(file)
        for academic_year, year_data in data.items():
            print(f"\nAcademic Year: {academic_year}\n------")
            for semester_data in year_data:
                for classes_data in semester_data["classes"]:
                    if keyword in classes_data:
                        print(classes_data[keyword])

def print_pre_reqs_from_JSON(JSON_file):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox()
    with open(JSON_file, "r") as file:
        data = json.load(file)
    for academic_year, year_data in data.items():
            print(f"\nAcademic Year: {academic_year}\n------")
            for semester_data in year_data:
                for classes_data in semester_data["classes"]:
                    try:
                        temp_url = str(classes_data["Class Link"])
                        
                        temp_url = fix_string(temp_url)
                        #print(temp_url) 
                        driver.get(url=temp_url)
                        try: 
                            paragraph_element = driver.find_element(By.XPATH, '/html/body/form/div[4]/div[2]/div[1]/div/div/div/p[2]')
                            print(f"!!!\n \"{classes_data['Class Name']}\" has a pre-req of :" )
                            print(f"{paragraph_element.text}\n\n")
                        except NoSuchElementException:
                            print(f"N\\A\n \"{classes_data['Class Name']}\" DOES NOT pre-req of : \n\n" )
                    except InvalidArgumentException:
                        print(f"N\\A\n \"{classes_data['Class Name']}\" has no link" )
    driver.quit()
                    
                    
def pre_req_tester():
    #URL = 'https://www.uml.edu/catalog/courses/COMP/2040'
    URL = 'https://www.uml.edu/catalog/courses/EECE/1070'
    driver = webdriver.Firefox()
    driver.get(url= URL)            
    try:
        paragraph_element = driver.find_element(By.XPATH, '/html/body/form/div[4]/div[2]/div[1]/div/div/div/p[2]')
        print(f"{paragraph_element.text}\n\n")  
    except NoSuchElementException:
        print("no exist element")
                        
def fix_string(input_str):
    string_a = str(input_str)
    string_a = string_a.replace("['", "")
    string_a = string_a.replace("']", "")            
    return string_a    

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

def write_f():
    #works fine
    with open(LOG_DATA_FILE_PATH, "w+") as file:
        file.write("Sample string 1!\n")
        file.write("Sample string 2!\n")
        
def main():
    #create_JSON_file()
    #print_JSON_file_data(JSON_DATA_FILE_PATH, CLASSES_KEY[2])
    print_pre_reqs_from_JSON(JSON_DATA_FILE_PATH)
    #pre_req_tester()
    #fix_string(['https://www.uml.edu/catalog/courses/EECE/1070'])
    #write_f()


main()
#end