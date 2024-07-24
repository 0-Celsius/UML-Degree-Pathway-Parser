#API to find all majors offered at UML
import requests
from bs4 import BeautifulSoup
import os


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
                base_link = r'https://www.uml.edu'
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
    print(f"\t {major_list[user_in].name}\n")
    return major_list[user_in]        
    
    
def continue_prompt():
    user_yn = input("options: 'y' or 'n': ")
    continue_inputs = ['y','yes']
    exit_inputs = ['n', 'no']
    desired_inputs = continue_inputs + exit_inputs
    
    
    while not user_yn.isalpha() or user_yn.lower() not in desired_inputs:
        user_yn = input("not right input, do 'y' or 'n': ")
    user_yn = user_yn.lower()
    
    if user_yn in exit_inputs:
        print("\n\nokay have a nice day!")
        exit


def find_degree_pathways(major_about_url):
    try:
        response = requests.get(major_about_url)   
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print('failed to lookup url: ', e)    
    
    try:
        a_elements = soup.find_all('a')
    except Exception as e:
        print(f"failed to find <a> elements: {e}")
    
    for a in a_elements:
        a_text = a.get('title','')
        #print(a_text)
        if 'pathway' in a_text.lower() and 'degree' in a_text.lower():
            #print(f"found a match: {a['href']}")
            
            return  r'https://www.uml.edu' + a['href']


def choose_pathway_option(choosen_major_option_url):
    try:
        response = requests.get(choosen_major_option_url)   
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"failed {e}")
        
    main_content = soup.find_all('div', {'class': 'comp-main-content__section__content'})
    
    # REALLY BAD PARSING HERE 
    # I was too lazy to figure another way to find all the elements so i went with this method
    # allows me to find the item quicker this way, at the cost of me making another parse for the methods
    offering_list = []
    for m_c in main_content:
        for content in m_c.find_all():
            if content.name == 'p':
                #print(content.text)
                offering_list.append("majortag: " + content.text)
            
            content_text = str(content.text).lower()
            if content.name == 'li' and 'concentration' in content_text:
                offering_name = content_text.rsplit('concentration')[0].title()
                #print(f"\t{offering_name}") 
                offering_list.append('cotag: ' + offering_name)
                
            if content.name == 'li' and 'option' in content_text:
                offering_name = content_text.rsplit('option')[0].title()
                #print(f"\t{offering_name}") 
                offering_list.append('cotag: ' + offering_name)
            
            
            if content.name == 'a' :
                offering_urls = r'https://www.uml.edu' + content['href']
                #print(f"\t\t{offering_urls}")
                offering_list.append(offering_urls)
        
    #print(offering_list)
    print()
     
    # really shit parse job by me, but not like we're iterating over this 100 times, so idrc
    cotag_skip_url = True
    majortag_skip_url = True
    index_1 = 0
    major_with_options_list = [] 
    for i in offering_list:
        if 'majortag: ' in i:
            txt = i.rsplit('majortag: ')[1]
            print(f'\n{txt}')
            majortag_skip_url = False
            
        if 'cotag: ' in i:
            txt = i.rsplit('cotag: ')[1]
            print(f'\t {txt}')
            cotag_skip_url = False
        
        if 'https://' in i and (not cotag_skip_url or not majortag_skip_url):
            # this will be hidden 
            print(f'\t\\-->[{index_1}]\t {i}')
            major_with_options_list.append(i)
            cotag_skip_url = True    
            majortag_skip_url = True
            index_1 += 1
    
    print('\n\n')
    #print(major_with_options_list)
    return major_with_options_list
        
def choose_major_prompt(list_of_options):
    max_len = len(list_of_options)
    print('choose an major you want: ')
    user_choice_n = int(input(f'enter a number(0 -> {max_len-1}): '))
    print(f'{type(user_choice_n)} :: {user_choice_n}')
    while not ( user_choice_n  in range(max_len)):
        user_choice_n = int(input(f'enter a number(0 -> {max_len-1}): '))    
        print(f'{type(user_choice_n)} :: {user_choice_n}')
        
    return list_of_options[user_choice_n]
        
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
            #print(f"index: {table_index}")
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
                    # we grab the course's data 
                    #print(f"\'{cell.get_text()}\'")
                    cell_text = cell.get_text()
                    if col_counter == 0: 
                        if '/' in cell_text: 
                            id_text = []
                            id_text_temp = cell_text.partition('/')
                            id_text.append(id_text_temp[0])
                            id_text.append(id_text_temp[2].strip('\n'))
                        else: 
                            id_text = cell_text
                        
                        a_ele_list = []
                        a_elements = cell.find_all('a')
                        for a in a_elements:
                            a_url = r'https://www.uml.edu' + a['href']
                            a_ele_list.append(a_url)
                        #print(a_ele_list)
                        
                        current_course.url = a_ele_list
                        current_course.IDs = id_text
                        
                        #print(f'url: {current_course.url}')
                        #print(f"id: \'{current_course.IDs}\'")                    
                    elif col_counter == 1:
                        if '/' in cell_text:
                            name_text = []
                            name_text_temp = cell_text.partition('/')
                            name_text.append(name_text_temp[0])
                            name_text.append(name_text_temp[2].strip('\n'))
                        else:
                            name_text = cell_text
                        current_course.name = name_text
                        #print(f"name: \' {current_course.name}\'")  
                    elif col_counter == 2:
                        if '/' in cell_text:
                            credit_text = []
                            credit_text_temp = cell_text.partition('/')
                            credit_text.append(credit_text_temp[0])
                            credit_text = credit_text_temp[2].strip('\n')
                        else:
                            credit_text = cell_text
                            
                        if '-' in cell_text:
                            credit_text = []
                            credit_text_temp = cell_text.partition('-')
                            credit_text = credit_text_temp[2]
                        current_course.credit = credit_text
                        #print(f"credits: \'{current_course.credit}\'")

                        # check data values 
                        
                        '''
                        print(f"id: \'{current_course.IDs}\'")
                        print(f"name: \' {current_course.name}\'")
                        print(f'url: {current_course.url}')
                        print(f"credits: \'{current_course.credit}\'")
                        '''
                        current_course_list.append(current_course)
                        current_course = Courses()   
                    else:
                        print("error")
                        pass 
                    col_counter +=1 
            #print('\n\n\n')
            #print('----------') 
        if current_course_list:
            #print('path is filled!!')
            pathway.append(Semester(semester_type, current_course_list))
        else:
            #print('pathway is empty?')
            pass
        current_course_list = []
    
     
    print('done running search!')
    return pathway

    
       
def print_pathway(pathway, base_year = 2022):
    for idx_year, semester  in enumerate(pathway, start= 1):
        total_val = 0
        class_index = 0 
        if idx_year % 2 == 0:
            base_year+=1
        
       
        print("||||||||||||||||||||||||||||||||||||||||")
        print((semester.name + ' ' + str(base_year)).center(40))
        print("||||||||||||||||||||||||||||||||||||||||")
        #print(semester.course_list)
        
        for course in semester.course_list:
            print(f"index: [{class_index}]\n")
            print(f"\t Class IDs: {course.IDs}")
            print(f"\t Class Name: {course.name}")
            
            print(f"\t Class url: {course.url}")
            print(f"\t Class credit: {course.credit}")
            print(f"\t Class about: {course.about}")
            print("|||>")
            print(" \\\\\\>")
            print("  |||>__")
            total_val += int(course.credit)
            class_index+=1 
        print(f"  >>>>[+] Total Classes: {class_index}")
        print(f"  >>>>[+] Total Credits: {total_val}")
        
        print("\n\n")
        
        
def generate_pathway_text_file(pathway, base_year = 2022, filename = 'pathway.txt'):
    
    generated_file_location = os.path.join(os.getcwd(), filename) 
    
    with open(generated_file_location, 'w') as w_file:
        for idx_year, semester  in enumerate(pathway, start= 1):
            total_val = 0
            class_index = 0 
            if idx_year % 2 == 0:
                base_year+=1
            
            
            w_file.write("|||||||||||||||||||||||||||||||||||||||| \n")
            w_file.write(f'{(semester.name + ' ' + str(base_year)).center(40)} \n')
            w_file.write("|||||||||||||||||||||||||||||||||||||||| \n")
            #print(semester.course_list)

            for course in semester.course_list:
                w_file.write(f"index: [{class_index}]\n")
                w_file.write(f"\t Class IDs: {course.IDs} \n")
                w_file.write(f"\t Class Name: {course.name} \n")
                
                w_file.write(f"\t Class url: {course.url} \n")
                w_file.write(f"\t Class credit: {course.credit} \n")
                w_file.write(f"\t Class about: {course.about} \n")
                
                w_file.write("|||> \n")
                w_file.write(" \\\\\\> \n")
                w_file.write("  |||>__ \n")
                total_val += int(course.credit)
                class_index+=1
            w_file.write(f"  >>>>[+] Total Classes: {class_index} \n")
            w_file.write(f"  >>>>[+] Total Credits: {total_val} \n")
            
            w_file.write("\n\n")
            
        
            

if __name__ == '__main__':
    
    #Tag: Options
    program = True
    return_txt_file = True
    
    if program:
        major_list = find_all_majors()
        choosen_major_about_url = user_terminal_interface(major_list)
        
        print("look up major's pathway?")
        continue_prompt()
        
        major_about_url = choosen_major_about_url.url
        
        
        major_options_url = find_degree_pathways(major_about_url)
    
        choosen_major_option_url_list = choose_pathway_option(major_options_url)
        
        choosen_major_option_url = choose_major_prompt(choosen_major_option_url_list)    

        pathway_requirements = search_url(url= choosen_major_option_url)
        
        if return_txt_file:
            generate_pathway_text_file(pathway_requirements)
            pass
        
        
    else:
        # just a quick path to look up a url/ my debugger
        pathway_url = ''
        
        #Double_EE_CS_URL = r"https://www.uml.edu/catalog/undergraduate/engineering/departments/electrical-computer-engineering/degree-pathways/dp-ece-eecs-2023.aspx"
        #user_pathway_url = Double_EE_CS_URL
         
        user_pathway_url = input("Please enter a pathway url from uml: ")
        pathway_url = user_pathway_url
        
        
        
        pathway_requirements = search_url(url = pathway_url)
        if return_txt_file:
            generate_pathway_text_file(pathway_requirements)
        
        '''
        A diagram of pathway:
        pathway:[N]                 [list]
            - semester:                 [class]
                - name:                     [str]
                - course_list:[N]           [list]
                    - courses:                  [class]
                        - name                      [list / str]
                        - id                        [list / str] 
                        - url                       [list / str]
                        - credit                    [int] 
                        - about                     [str]
                    - courses:                  [class]
                        - name                      [list / str]
                        - id                        [list / str] 
                        - url                       [list / str]
                        - credit                    [int] 
                        - about                     [str]
                    - courses:                  [class]
                        - name                      [list / str]
                        - id                        [list / str] 
                        - url                       [list / str]
                        - credit                    [int] 
                        - about                     [str]
                    - ... 
        '''
        print_pathway(pathway_requirements)
 