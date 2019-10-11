# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 17:59:30 2019

@author: Jason
"""
import json
from classes import Course,Offering

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
    line = line.replace(')','')
    line = line.replace('Not yet complete','')
    return line


def add_multiple_classes(line): 
    '''Deals with lines that are like ECON20, 21, 22.'''                                
    offered_courses = {}

    courses = line.split(',')
    for course in courses:          
        if any(dept in course for dept in departments):    
            course_info = course.split()
            if course_info[-1] == 'or' or course_info[-1] == 'and':            
                department = course_info[0]
                course_num = course_info[1]    
                offered_courses[department] = [course_num]   
                offered_courses['option'] = True
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
    '''Deals with lines only containing one class. Ex: 1 Class in ECON 20.'''
    offered_courses = {}

    requirement = line.split()                             
    for dept in departments:       
        if dept in requirement:
            if requirement[-1] == 'and' or requirement[-1] == 'or':
                offered_courses['option'] = True
                course_num = requirement[-2]
                offered_courses[dept] = [course_num]
            else:
                course_num = requirement[-1]
                offered_courses[dept] = [course_num]

    offered_courses = expand_courses(offered_courses)
    offered_courses = schedule_checker(offered_courses)    
    return offered_courses


def create_master_requirement(all_courses, lines, i):
    '''Initializes master requirement with empty list. Sub requirements will eventually populate the list.'''
    master_req = clean_line(lines[i-1])
    all_courses.append([master_req,[]])    

def add_to_master_requirement(all_courses, i, lines, offered):
    '''Add sub requirement to its respective overall requirement.'''
    if 'Lower-Division Writing' in all_courses[-1][0]:                                    
        if 'Choose' in lines[i-2]:
            not_complete = clean_line(lines[i-3])                        
            all_courses[-1][1].append([not_complete,offered])                           
            
        # else:
        #     all_courses[-1][1][1].update(offered)
    else:
        for x in range(15):                                       
            if 'yet' in lines[i-x]:
                not_complete = clean_line(lines[i-x])                        
                all_courses[-1][1].append((not_complete,offered))                           
                break


def add_standalone_requirement(all_courses, line, i, lines):
    '''Deals with a requirement that has no sub requirements. Adds requirement + courses to all_courses list.'''
    master_req = clean_line(lines[i-1])
    if ',' in line:
        offered = add_multiple_classes(line)                                                                                                            

    else:
        offered = add_single_class(line)    
    all_courses.append([master_req,[offered]])


def read_input(degreeworks_data):
    '''Takes user input of their degreeworks and outputs list of all requirements 
    with the associated courses that are offered for current quarter.'''                                
    all_courses = []
    lines = degreeworks_data.splitlines()
    for i,line in enumerate(lines):
        line = clean_line(line)                                                  
        if 'Still' in line and 'Class' in line:                                 
            add_standalone_requirement(all_courses, line, i, lines)

        elif 'Still' in line:
            create_master_requirement(all_courses, lines, i)

        elif 'Class' in line:                              
            if ',' in line:                                 
                offered_courses = add_multiple_classes(line)        

            else:
                offered_courses = add_single_class(line)

            if offered_courses is not None:
                add_to_master_requirement(all_courses, i, lines, offered_courses)    
    return all_courses
    

def add_ranges(course, course_nums):
    '''Adds ranges of classes to dictionary. Ex: ECON 20:25'''
    numbers = course.split(':')
    start = int(numbers[0])
    end = int(numbers[1])
    for x in range(start,end+1):                                   
        course_nums.append(str(x))  
    
    #TODO add return logic
    

def add_unknowns(course, course_list):
    '''Adds classes that could be any number or letter. Ex: ECON 10@'''
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
    
    #TODO add return logic 
 

def expand_courses(courses):
    '''reads requirements dict and if theres 111:121 or 12@ then it updates dict to include additional course numbers.'''
    for department in courses.values():  
        if type(department) is not bool:           
            for course in department:            
                if ':' in course:
                    add_ranges(course, department)
                    department.remove(course) 
    
                elif '@' in course: 
                    add_unknowns(course, department)
                    department.remove(course)
            
    return courses

                    
def schedule_checker(courses): 
    '''takes courses dict from each line and returns only the courses that are offered as a list'''  #this static file is the pre-downloaded schedule of classes and will be updated at some constant interval
    offered = []

    with open('soc.json','r') as f:
        soc = json.load(f)
        for dept in courses:
            if dept != "option":
                for course in soc[dept]:
                    if course['num'] in courses[dept]:
                        offered.append((dept,course)) 
    if 'option' in courses and len(offered) > 0:
        offered.append('True')
    return offered


if __name__ == '__main__':
    degreeworks = input()
    read_input(degreeworks) 
        
            
            