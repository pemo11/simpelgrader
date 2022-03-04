# file: GradeAction.py
from datetime import datetime

'''
Defines a single grading action for the grade report
'''
class GradeAction:

    def __init__(self, type):
        self.timestamp = datetime.now()
        self.type = type
        self.description = "None"
        self.result = ""

    def __repr__(self):
        return f"Type: {self.type}"