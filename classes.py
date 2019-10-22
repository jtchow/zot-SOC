#Requirement classes
class Requirement:
    '''Requirement to fulfill part of the degree \n
    classes structure: { DEPT: [ Course1, Course2 ] }
    '''
    def __init__(self, name, classes):
        self.name = name
        self.classes = classes
        self.is_master_req = False
        self.is_sub_req = False
        self.is_empty = True

class SingleRequirement(Requirement):
    '''Any big requirement that doesn't have sub-requirements. Same level as MasterRequirement'''

class MasterRequirement:
    '''Could have one or multiple subrequirements to fulfill it.\n
    fulfilled_by is a list of Requirement objects.'''
    def __init__(self, name):
        self.name = name
        self.fulfilled_by = []  
        self.is_master_req = True
        self.is_empty = True

class SubRequirement():
    ''' fulfill part of a requirement '''
    def __init__(self, name):
        self.name = name
        self.fulfilled_by = []
        self.is_sub_req = True
        self.is_empty = True
        
#Course classes
class Course:
    ''' example: ECON 20A  Microeconomics\n
        num = '20A'\n
        title = microeconomics,\n
        offerings = list of offering objects (the lectures and discussions)'''
    # def __init__(self, num: str, title, offerings):       
    #     self.num = num
    #     self.title = title
    #     self.offerings = offerings

    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)



class Offering:
    ''' offering is either a lecture, discussion, or lab. all attributes come from SOC. examples: time, place, prof etc'''
    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)

        