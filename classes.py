#Requirement classes
class Requirement:
    '''Any requirement that doesn't have sub requirements.\n
    fulfilled_by structure: { DEPT: [ Course1, Course2 ] }
    '''
    def __init__(self, name):
        self.name = name
        self.fulfilled_by = {}

class MasterRequirement:
    '''Has multiple choices to fulfill it.\n
    fulfilled_by is a list of SubRequirement objects.'''
    def __init__(self, name):
        self.name = name
        self.fulfilled_by = []  

class SubRequirement(Requirement):
    ''' fulfill part of a requirement '''
    pass



#Course classes
class Course:
    ''' example: ECON 20A  Microeconomics\n
        num = '20A'\n
        title = microeconomics,\n
        offerings = list of offering objects (the lectures and discussions)'''
    def __init__(self, num: str, title):       
        self.num = num
        self.title = title
        self.offerings = []



class Offering:
    ''' offering is either a lecture, discussion, or lab. all attributes come from SOC. examples: time, place, prof etc'''
    def __init__(self, iterable=(), **kwargs):
        self.__dict__.update(iterable, **kwargs)
        