#run:  DegreePathwayWebParser-env\Scripts\activate
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

ACADEMIC_YEAR_KEY = ['Freshman year', 'Sophomore year', 'Junior year', 'Senior year']
CLASSES_KEY = ["Class Name", "Class ID", "Class Link", "Credit(s)"]

JSON_FILES_FOLDER_PATH = 'T:\WalnutShrimp\py - Degree Pathway Web Parser\JSON Files'
JSON_DATA_FILE_PATH = JSON_FILES_FOLDER_PATH + "\\" +"data.json"

def print_JSON_file_data(JSON_file, keyword):
    with open(JSON_file, "r") as file:
        data = json.load(file)
        for academic_year, year_data in data.items():
            print(f"\nAcademic Year: {academic_year}\n------")
            for semester_data in year_data:
                for classes_data in semester_data["classes"]:
                    if keyword in classes_data:
                        print(classes_data[keyword])


def main():
    print_JSON_file_data(JSON_DATA_FILE_PATH, CLASSES_KEY[0])
    
    
main()
#end