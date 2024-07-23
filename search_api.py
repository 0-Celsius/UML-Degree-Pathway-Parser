#API to find all majors offered at UML
import requests
from bs4 import BeautifulSoup

import time


ALL_MAJOR_URL = r'https://www.uml.edu/catalog/undergraduate/majors.aspx'

class Undergrad_Major:
    def __init__(self, name = 'empty major', abbreviation = None, url = None, concentrations = None):
        self.name = name
        self.type = type
        self.abbreviation = abbreviation
        self.url = url
        self.concentrations = concentrations

class Courses:
    def __init__(self, name = None, IDs = None, url = None, credit = None, about = None):
        self.name = name 
        self.IDs = IDs
        self.url = url
        self.credit = credit 
        self.about = about

class Semester:    
    def __init__(self, name = 'empty semester', course_list = None):
        self.name = name
        self.course_list = course_list

def find_all_majors():
    total_time = time.perf_counter()
    
    all_majors_url = ALL_MAJOR_URL
    response = requests.get(all_majors_url)   
    soup = BeautifulSoup(response.content, 'html.parser')
    main_content = soup.find('div', {'class': 'comp-main-content__section__content'})
        
    return_list_ = []
    
    ul_elements = main_content.find_all('ul')

    
    for ul in ul_elements:
        #print(f'ul: {ul.get_text()}')
        for li in ul:
            
            # gets the li string to use: 
            
            li_text = str(li.get_text())
            li_text_partition = li_text.partition(':')
            major_name = li_text_partition[0]
            
            # ignores the li that just options in a 
            ignore_words_filter = ['option', 'concentration']
            if any(word in major_name.lower() for word in ignore_words_filter):
                #print(f'skipped: {li_text}')
                break
            
            abbr_partition = li_text_partition[2].partition('\n')
            
            abbr = abbr_partition[0]
            options = []
            
            
            try:
                # looks to find all the major's options/concentration
                
                inner_ul = li.find('ul')
                inner_lis_list = inner_ul.find_all('li')
                
                for in_lis in inner_lis_list:
                    in_lis_text = in_lis.get_text()
                    options.append(in_lis_text)
            except Exception as e:
                #print(f'error: {e}\n')
                pass    
            link = ''
            try:
                # gets the link 
                base_link = r'uml.edu'
                link = base_link + li.find('a')['href']
            except Exception as e:
                #print(f'error: {e}\n')
                pass 
            
            #print(f'li text: {li_text}')
            '''
            print(f'major_name text: {major_name}')
            print(f'abbr text: {abbr}')
            print(f'options text: {options}')
            print(f'href: {link}')
            print('\n\n')
            '''
            return_list_.append(Undergrad_Major(name= major_name,
                                                abbreviation= abbr,
                                                url= link,
                                                concentrations= options))
    
    total_time = time.perf_counter() - total_time
    print(f"total time: {total_time}")
    return return_list_ 
  
             
def user_terminal_interface(major_list):
    if major_list:
        pass
    else: 
        print(f"no list proved")

    
    # prints all the majors
    for idx, major in enumerate(major_list):
        major_with_index = f'[{idx}] '+ major.name
        if (idx + 1) % 2:
            print('{:60}'.format(major_with_index), end='\t\t')
        else:
            print(major_with_index, end='\n')
    
    user_in = input("\n\nplease choose the major's pathway you want to look at: ")
    
    while user_in.isdigit() not in range(len(major_list)):    
        user_in = input("retry please: ")
        print(f"[{user_in}]")
    
    user_in = int(user_in)
    print("choosen major is:")
    print(major_list[user_in].name)
    return major_list[user_in]        
    
    
def continue_prompt():
    user_yn = input("look up major's pathway?\noptions: 'y' or 'n': ")
    continue_inputs = ['y','yes']
    exit_inputs = ['n', 'no']
    desired_inputs = continue_inputs + exit_inputs
    
    
    while not user_yn.isalpha() or user_yn.lower() not in desired_inputs:
        user_yn = input("not right input, do 'y' or 'n': ")
    user_yn = user_yn.lower()
    
    if user_yn in exit_inputs:
        print("\n\nokay have a nice day!")
        exit


def search_url(major = None, url = None):
    '''
    params:
        - Major: takes in a major class
        - Takes in a URL
    '''        
    url_value = '' 
    if url:        
        url_value = url
    elif major:
        url_value = major.url
    else:
        print("no value")
        exit



    response = requests.get(url_value)   
    soup = BeautifulSoup(response.content, 'html.parser')

    # list of the semester, [fall, spring, fall, spring, etc]
    pathway = []
    
    tables = soup.find_all('table')
    for table_index,table in enumerate(tables):
        #--works
        current_course_list = []
        semester_type = 'Fall Semester' if table_index % 2 == 0 else 'Spring Semester'
        
        # looks for the course's and their values
        rows = table.find_all('tr')
        #print(rows)
        for row in rows:
            cells = row.find_all('td')
            
            
            col_counter = 0 
             
            current_course = Courses()
            
            # list values to store misc data 
            course_IDs_list = []
            course_urls_list = []
            
            
            for cell in cells:
                '''
                0: ID 
                1: Name
                2: Credit
                '''
                if ((cell.get_text().isdigit()) and (int(cell.get_text()) >= 10)) or cell.get_text().lower() == 'total':
                    # skips the total credit things: 'total' and credit >= 10 
                    #print(f"skipped: {cell.get_text()}")
                    pass
                else:
                    # has the conditions we want
                    #print(f"\'{cell.get_text()}\'")
                
                    if col_counter == 0:
                        print(f"id:\'{cell.get_text()}\'")
                        try: 
                            cell.get_text().partition('')
                            
                        
                    elif col_counter == 1:
                        print(f"name: \' {cell.get_text()}\'")
                
                    elif col_counter == 2:
                        print(f"credits: \'{cell.get_text()}\'")
                
                    else:
                        print("error")
                        pass     
                    
            print('\n\n\n')
            print('----------') 
        # Creates a semester
        '''
        for row in rows:
            
            cells = row.find_all('td')
            print(cells)

            
            col_counter = 0 
             
            current_course = Courses()
            
            # list values to store misc data 
            course_IDs_list = []
            course_urls_list = []
            
            for cell in cells:
                # checks if its the total value, if so ignore
                if (cell.get_text() == "Total") or ((cell.get_text().isdigit()) and (int(cell.get_text()) >= 8)):
                    pass
                else:
                    try: 
                        a_elements = cell.find_elements('a')
                    except:
                        print("fail to find class's <a> content")
                           
                            
                            
                    if a_elements:
                        for a in cell.find_elements('a'):
                            #base_link = r'uml.edu'
                            course_IDs_list.append(a.get_text())
                            course_urls_list.append(r'uml.edu' + a['href'])

                    else:
                        if col_counter == 1:
                            current_course.name = cell.text
                        if col_counter == 2:
                            current_course.IDs = course_IDs_list
                            current_course.url = course_urls_list
                            current_course.credit = cell.text
                            current_course_list.append(current_course)
                        if cell.text.isdigit():
                            pass
                col_counter += 1
            current_course = Courses()
        # creates the semester
        current_semester = Semester(name = semester_type, course_list= current_course_list) 
        current_course_list = []
        pathway.append(current_semester)
        '''
    print('done running search!')
    return pathway


def print_pathway(pathway):
    base_year = 2022
    
    for idx_year, semesters in enumerate(pathway, start= 1):
        if idx_year % 2 == 0:
            base_year+=1

        for idx_semesters, semester in enumerate(semesters):
            current_semester = semesters[idx_semesters].name 
            print(f"Current semester: {current_semester} {base_year}")


            for course in enumerate(semester):
                print(f"\t Class Name: {course.name}")
                print(f"\t Class IDs: {course.IDs}")
                print(f"\t Class url: {course.url}")
                print(f"\t Class credit: {course.credit}")
                print(f"\t Class about: {course.about}")
                
                
                    

if __name__ == '__main__':
    program = False 
    if program:
        major_list = find_all_majors()
        choosen_major = user_terminal_interface(major_list)
        choosen_major = "test"
        continue_prompt()
        search_url(choosen_major)
        
    else:
        # just a quick path to look up a url/ my debugger
        Double_EE_CS_URL = r"https://www.uml.edu/catalog/undergraduate/engineering/departments/electrical-computer-engineering/degree-pathways/dp-ece-eecs-2023.aspx"
        pathway = search_url(url = Double_EE_CS_URL)
        #print(pathway[0].name)
        #print(pathway[0].name.course_list)
        #print_pathway(pathway)
