#run:  DegreePathwayWebParser-env\Scripts\activate
import json
import time
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
LOG_DATA_FILE_PATH = LOG_FILES_FOLDER_PATH + "\\" +"schedule.txt"

# URL related functions
def get_URL():
    
    #URL = 'https://www.uml.edu/catalog/undergraduate/engineering/departments/electrical-computer-engineering/degree-pathways/dp-ece-eecs-2023.aspx'
    '''
    UNDERGRADUATE_URL= "https://www.uml.edu/catalog/undergraduate"
    URL = input("please input an undergraduate degree pathway to parse: ")
    while(UNDERGRADUATE_URL not in URL):
        URL = input("please input an undergraduate degree pathway to parse: ")
    '''    
    Chem_Forensic_URL = r"https://www.uml.edu/catalog/undergraduate/sciences/departments/chemistry/degree-pathways/dp-chemistry-forensic-science-2020.aspx"
    CS_General_URL = r"https://www.uml.edu/catalog/undergraduate/sciences/departments/computer-science/degree-pathways/dp-cs-general-2020.aspx"
    Double_EE_CS_URL = r"https://www.uml.edu/catalog/undergraduate/engineering/departments/electrical-computer-engineering/degree-pathways/dp-ece-eecs-2023.aspx"
    Sound_recording_URL = r"https://www.uml.edu/catalog/undergraduate/fahss/departments/music/degree-pathways/dp-srt-2022.aspx"
    Excerise_science_URL = r"https://www.uml.edu/catalog/undergraduate/health-sciences/departments/physical-therapy/degree-pathways/dp-pt-es-clinical-2021.aspx"
    
    
    URL = Excerise_science_URL
    
    return URL

def get_pathway_name(IN_url):
    return (IN_url.rsplit('/',1)[1]).rsplit(".")[0]
    

              
# JSON related functions                   
def fix_string(input_str):
    string_a = str(input_str)
    string_a = string_a.replace("['", "")
    string_a = string_a.replace("']", "")            
    return string_a    

def create_JSON_file(IN_url):
    print("creating JSON file!")
    
    driver = webdriver.Firefox()
    driver.get(url=IN_url)
    
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



#print functions
def print_JSON_file_data(JSON_file, keyword):
    print("printing JSON file in terminal!\n\n")
    
    with open(JSON_file, "r") as file:
        data = json.load(file)
        for academic_year, year_data in data.items():
            print(f"\nAcademic Year: {academic_year}\n------")
            for semester_data in year_data:
                for classes_data in semester_data["classes"]:
                    if keyword in classes_data:
                        print(classes_data[keyword] )

def print_pre_reqs_from_JSON(JSON_file):
    print("printing pre reqs file in terminal!\n\n")
    
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



#text file related functions
def create_text_file(JSON_file):
    print("making text file!")
    
    headless_option = 0
    terminal_print_option = 1
    credits_total_option = 1
    
    
    
    if headless_option == 1: 
        options = Options()
        options.add_argument("--headless")
        
        driver = webdriver.Firefox(options = options)
    else:     
        driver = webdriver.Firefox()
        
        
    # reads the JSON file   
    with open(JSON_file, "r") as file:
        
        #opens where we're create/storing the final text file
        text_file_location = "schedule.txt"
        #text_file_location = LOG_DATA_FILE_PATH
        
        with open(f"{text_file_location}","w") as w_file:
            data = json.load(file)
            
            #opens the JSON file: "academic years" and their "year data"
            for academic_year, year_data in data.items():
                
                #terminal print option: 
                if terminal_print_option == 1:
                    print(f"Grabbing Academic Year: {academic_year}",end="\n")
                
                w_file.write(f"\nAcademic Year: {academic_year}\n------\n")
                
                
                for semester_data in year_data:
                    
                    #if we want the counter option for credits
                    if credits_total_option == 1: 
                        credit_total_val = 0 
                    
                    #terminal print option: 
                    if terminal_print_option == 1:
                        print(f" Semester: {semester_data['Semester']}", end="\n\n")
                    
                    w_file.write(f"{semester_data['Semester']} :\n--- \n")
                    
                    
                        
                    for classes_data in semester_data["classes"]:
                        #terminal print option: 
                        if terminal_print_option == 1:
                                print(f"trying: {classes_data["Class Name"]}", end="")
                                start_time = time.time()
                    
                        try:        
                            temp_url = str(classes_data["Class Link"])
                            temp_url = fix_string(temp_url) 
                            driver.get(url=temp_url)
                            try: 
                                paragraph_element = driver.find_element(By.XPATH, '/html/body/form/div[4]/div[2]/div[1]/div/div/div/p[2]')
                                #print(f"!!!\n \"{classes_data['Class Name']}\" has a pre-req of :" )
                                #print(f"{paragraph_element.text}\n\n")
                                w_file.write(f"!!!\n \"{classes_data['Class Name']}\" has a pre-req of :" )
                                w_file.write(f"{paragraph_element.text}")
                                
                            except NoSuchElementException:
                                #print(f"N\\A\n \"{classes_data['Class Name']}\" DOES NOT pre-req of : \n\n" )
                                w_file.write(f"N\\A\n \"{classes_data['Class Name']}\" DOES NOT pre-req of :")
                        except InvalidArgumentException:
                            #print(f"N\\A\n \"{classes_data['Class Name']}\" has no link" )
                            w_file.write(f"N\\A\n \"{classes_data['Class Name']}\" has no link" )
                        
                        if credits_total_option == 1:
                            credit_total_val += int(classes_data['Credit(s)'])
                            w_file.write(f"\n\t:: Credit: {classes_data['Credit(s)']}\n{credit_total_val}\n")
                        else: 
                            w_file.write(f"\n\t:: Credit: {classes_data['Credit(s)']}\n\n")
                           
                        #terminal print option: 
                        if terminal_print_option == 1:
                            elapsed_t =  (time.time() - start_time) * 1000
                            elapsed_t = "{:.2f}".format(elapsed_t)
                            print(f"\ttime: {elapsed_t} ms \n  url: {classes_data["Class Link"]}", end="\n")
                     
                            
                    #terminal print option: 
                    if terminal_print_option == 1:
                        print("\n\n")
                    w_file.write("\n\n")    
                                
                #terminal print option: 
                if terminal_print_option == 1:
                    print("\n\n")
                w_file.write("\n\n\n\n\n")
    print("done making text file!")
    driver.quit()      
   
        

if __name__ == '__main__':
 
    # Creates the JSON File
    
    url = get_URL()
    print(f"Creating the JSON File for the following path:\n\n\t\t \"{get_pathway_name(url)}\"\n")
    print(f" url: {url}")
    
    checker = input("\n\nproceed? (y/n):\n")    
    
    
    if checker == 'y':
        create_JSON_file(url)
    else: 
        exit()
    print("")
        
    '''
    #print functions to print out data
        print_JSON_file_data(JSON_DATA_FILE_PATH, CLASSES_KEY[2])
        print_pre_reqs_from_JSON(JSON_DATA_FILE_PATH)
    
    '''
    
    create_text_file(JSON_DATA_FILE_PATH)
    
    print("Done With program!")
#end