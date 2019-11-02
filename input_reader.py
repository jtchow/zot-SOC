# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 17:59:30 2019

@author: Jason
"""
import json
from classes import *

departments = ['ACENG','AFAM','ANATOMY','ANESTH','ANTHRO','ARABIC','ARMN','ART HIS','ARTS','ARTSHUM','ASIANAM','BANA','BATS','BIOSCI','BIOCHEM','BME',
               'CAMPREC','CBEMS','CBE','CEM','CHC/LAT','CHEM','CHINESE','CLASSIC','CLT&THY','COGS','COMLIT','COMPSCI','CRITISM','CRM/LAW','CSE','DANCE','DERM','DEV BIO','DRAMA',
               'EASIAN','EARTHSS','ECOEVO','ECON','ECPS','EDAFF','EDUC','EECS','EHS','ENGLISH','ENGRCEE','ENGRMAE','ENGRMSE','ENGR','EPIDEM','ER MED','EUROST','FAMMED','FIN',
               'FLM&MDA','FRENCH','GEN&SEX','GERMAN','GLBLME','GLBLCLT','GREEK','HEBREW','HINDI','HISTORY','HUMAN','HUMARTS','I&CSCI','IN4MATX','INT MED','INTLST',
               'ITALIAN','JAPANSE','KOREAN','LATIN','LAW','LINGUIS','LITJRN','LPS','M&MG','MATH','MED','MED ED','MED HUM','MGMT','MGMTEP','MGMTHC','MGMTFE',
               'MGMTMBA','MGMTPHD','MICBIO','MOLBIO','MPAC','MSE','MUSIC','NETSYS','NEURBIO','NEUROL','NURSCI','OB/GYN','OPHTHAL','PATH','PEDGEN','PEDS','PERSIAN',
               'PHARM','PHILOS','PHRMSCI','PHYSCI','PHYSICS','PHYSIO','PLASTIC','PM&R','POLSCI','PORTUG','PSYBEH','PSYCH','PUBPOL','PUBHLTH','RADIO','RELSTD','ROTC',
               'RUSSIAN','SOCSCI','SOCECOL','SOCIOL','SPANISH','SPPS','STATS','SURGERY','TAGALOG','ART','TOX','UCDC','UNIAFF','UNISTU','UPPP','VIETMSE','VISSTD','WRITING']


def clean_line(line):
    line = ''.join(s for s in line if ord(s)>31 and ord(s)<126)
    line = line.replace('(','')
    line = line.replace(')','')
    line = line.replace('Not yet complete','')
    line = line.replace('Credits >= 4 ','')  
    return line


def add_multiple_classes(line): 
    """Deals with input lines that contain multiple classes. Ex: ECON20, 21, 22, ENGR1, 2, 3 """                                
    offered_courses = {}

    courses = line.split(',')
    for course in courses:          
        if any(dept in course for dept in departments):    
            course_info = course.split()
            if course_info[-1] == 'or' or course_info[-1] == 'and':            
                department = course_info[0]
                course_num = course_info[1]    
                offered_courses[department] = [course_num]   
                offered_courses = expand_courses(offered_courses)                      
                offered_courses = schedule_checker(offered_courses)
                return offered_courses

            else: 
                department = course_info[-2]
                course_num = course_info[-1]                    
                offered_courses[department] = [course_num]    

            last_dept_seen = department
                             
        else:
            course_num = course.strip()
            offered_courses[last_dept_seen].append(course_num)

    offered_courses = expand_courses(offered_courses)                      
    offered_courses = schedule_checker(offered_courses)
    return offered_courses


def add_single_class(line):
    """Deals with lines only containing one class. Ex: 1 Class in ECON 20."""
    offered_courses = {}

    requirement = line.split()                             
    if requirement[-1] == 'and' or requirement[-1] == 'or':
        course_num = requirement[-2]
        dept = requirement[-3]
    else:
        course_num = requirement[-1]
        dept = requirement[-2]
        
    if course_num[0].isdigit():
        offered_courses[dept] = [course_num]

    offered_courses = expand_courses(offered_courses)
    offered_courses = schedule_checker(offered_courses)  
    return offered_courses


def create_master_requirement(all_courses, lines, i):
    """Creates master requirement object with a fulfilled_by attribute that is an empty list. 
    Sub requirements will eventually populate the list."""
    #if you've already completed a class towards the requirement, the name is somewhere above 
    if lines[i-1].split()[0] in departments:
        for x in range(15):
            if 'yet' in lines[i-x]:
                requirement_name = clean_line(lines[i-x])
                break  
    #if you haven't then the name is the previous line
    else:
        requirement_name = clean_line(lines[i-1]) 
        master_req = MasterRequirement(requirement_name)
        all_courses.append(master_req)
        

def add_to_bigger_requirement(all_courses, i, lines, offered, choose_number):
    """Add sub requirement to its respective overall requirement."""
    still_needed = clean_line(lines[i]).split()
    still_needed_num = still_needed[2]
    for x in range(15):                                                                     #arbitrary range                           
        if 'yet' in lines[i-x]:                                                             #"yet" marker denotes the name of a requirement. Example: "Not yet complete: Econ 20"
            name = clean_line(lines[i-x])                      
            req = Requirement(name, still_needed_num, offered)  
            if choose_number > 0:        
                all_courses[-1].fulfilled_by[-1].fulfilled_by.append(req)
                break
            else:
                all_courses[-1].fulfilled_by.append(req) 
                break


def add_single_requirement(all_courses, line, i, lines):
    """Adds a requirement that has no sub requirements to the all_courses list."""
    if ',' in line:
        offered = add_multiple_classes(line)                                                                                                          
    else:
        offered = add_single_class(line)  
        
    still_needed = lines[i].split()
    still_needed_num = still_needed[2]
    #if you've already completed a class towards the requirement
    if lines[i-1].split()[0] in departments:
        for x in range(15):
            if 'yet' in lines[i-x]:
                requirement_name = clean_line(lines[i-x])
                break  
    #if you haven't
    else:
        requirement_name = clean_line(lines[i-1])         
      

    requirement = SingleRequirement(requirement_name, still_needed_num, offered)
    all_courses.append(requirement)
    
def get_choose_number(line):
    """Gets number from line 'Choose 2 from the following' to make adding sub sub requirements easier"""
    line_info = line.split()
    choose_number = int(line_info[2])
    return choose_number

def create_sub_requirement(all_courses, lines, i):
    requirement_name = clean_line(lines[i-1])
    sub_req = SubRequirement(requirement_name)
    all_courses[-1].fulfilled_by.append(sub_req)  


def empty_checker(all_requirements):
    """Checks whether or not requirements are empty to make output easier"""
    for big_requirement in all_requirements:   
        if type(big_requirement) == MasterRequirement:
            for small_req in big_requirement.fulfilled_by:
                if type(small_req) == SubRequirement:
                    for req in small_req.fulfilled_by:
                        if len(req.classes) != 0:
                            req.is_empty = False
                            small_req.is_empty = False
                            big_requirement.is_empty = False
                else:
                    if len(small_req.classes) != 0:
                        big_requirement.is_empty = False
                        small_req.is_empty = False
                    

        elif type(big_requirement) == SingleRequirement:
            if len(big_requirement.classes) != 0:
                big_requirement.is_empty = False


def read_input(degreeworks_data):
    """Takes user input and outputs their degree requirements 
    and only the relevant courses that are offered next quarter."""                                
    all_requirements = []
    lines = degreeworks_data.splitlines()
    choose_number = 0
    #started = False
    
    for i,line in enumerate(lines):
        #if started:
            line = clean_line(line)                 

            #Ex: "Still needed: 1 class in Econ20"                                 
            if 'Still' in line and 'Class' in line:                                 
                add_single_requirement(all_requirements, line, i, lines)

            #Ex: "Still needed: 3 classes Category IV"
            elif 'Still' in line:
                create_master_requirement(all_requirements, lines, i)

            elif 'Choose' in line:
                create_sub_requirement(all_requirements,lines,i)
                choices = get_choose_number(line)
                choose_number += choices
                

            elif 'Class' in line and 'in' in line:  
                #Ex: "2 classes in Econ20, 21, 22"                            
                if ',' in line:                                 
                    offered_courses = add_multiple_classes(line)   

                #Ex: "1 classes in Econ20"
                else:
                    offered_courses = add_single_class(line)

                if offered_courses is not None:
                    add_to_bigger_requirement(all_requirements, i, lines, offered_courses, choose_number)  
                    if choose_number > 0:
                        choose_number -= 1
        # else:
        #     if 'General Education Requirements' in line:
        #         started = True

    empty_checker(all_requirements)
    return all_requirements
    

def add_ranges(course, course_list):
    """Adds ranges of classes. Ex: ECON 20:25"""
    numbers = course.split(':')
    start = int(numbers[0])
    end = int(numbers[1])
    for x in range(start,end+1):                                   
        course_list.append(str(x))  
    

def add_unknowns(course, course_list):
    """Adds classes that could be any number or letter. Ex: ECON 10@"""
    alphabet = ['A','B','C','D','E','F']
    
    if int(course[0]) > 1:
        for letter in alphabet:
            new_course = str(course[0:2])+letter
            course_list.append(new_course)

    elif len(course) <= 3: 
        for x in range(0,10):
            new_course = str(course[0:2]) + str(x)
            course_list.append(new_course)

    else:
        for letter in alphabet:
            new_course = str(course[0:3])+letter
            course_list.append(new_course)
            
def add_honors_unknowns(course, course_list):
    """Adds classes that could be any number or letter. Ex: ECON 10@"""
    alphabet = ['A','B','C','D','E','F']
    for x in range(0,10):    
        tens_new_course = str(course[0:2]) + str(x)
        course_list.append(tens_new_course)
        for letter in alphabet:
            new_course = tens_new_course + letter
            course_list.append(new_course)
        for i in range(0,10):
            hundreds_new_course = tens_new_course + str(i)
            for letter in alphabet:
                new_course = hundreds_new_course + letter
                course_list.append(new_course)
        



def expand_courses(courses):
    """reads requirements dict and updates it for special cases to include additional course numbers."""
    for department_courses in courses.values():  
        for course in list(department_courses):        
            if ':' in course:
                add_ranges(course, department_courses)
                department_courses.remove(course) 

            elif '@' in course: 
                if course[0] != 'H':
                    add_unknowns(course, department_courses)
                else:
                    add_honors_unknowns(course,department_courses)
                department_courses.remove(course)
            
    return courses

                    
def schedule_checker(courses): 
    """takes courses dict and returns only the courses that are offered"""  #this static file is the pre-downloaded schedule of classes and will be updated at some constant interval
    offered = {}

    with open('soc.json','r') as f:
        soc = json.load(f)
        for dept in courses:
            for course in soc[dept]:
                if course['num'] in courses[dept]:
                    course = Course(course)
                    if dept in offered:
                        offered[dept].append(course) 
                    else:
                        offered[dept] = [course]
    return offered


if __name__ == '__main__':
    degreeworks = input()
    read_input(degreeworks) 
    
            
            