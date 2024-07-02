import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidArgumentException

                       
def fix_string(input_str):
    string_a = str(input_str)
    string_a = string_a.replace("['", "")
    string_a = string_a.replace("']", "")            
    return string_a    

def get_pre_reqs(JSON_file):
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
   
   