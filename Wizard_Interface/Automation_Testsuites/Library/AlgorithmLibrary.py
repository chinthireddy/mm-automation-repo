from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import re
import os
import random
from operator import contains
from itertools import imap, repeat
import calendar
import csv
import win32clipboard
import time
import calendar
from datetime import datetime, time, date
from datetime import datetime
from datetime import date
import time
import datetime
import os
import xlrd
import CommonLibrary
class AlgorithmLibrary:

        CorrectAnswerDictionary = {}
        
        def __init__(self):
                pass

        def debug(self):
            return                


        def answer_the_mc_question(self, png, performance):
            """ Returns the answer to use for a multiple choice question """
            """ In this version, a random answer is given to save time """
            """ The answer is a number from 0 to 3 """
            correct_answer = CorrectAnswerDictionary[png]
            correct_code = { 'A':0, 'B':1, 'C':2, 'D':3 }[correct_answer]
            r1 = random.random() * 100
            log = ''
            if r1 <= performance:
               log =   'The correct answer, ' + str(correct_answer) + ', is given.  The random value was ' + str(r1)
               return [ correct_code, log ]
            other_values = { 0:[1, 2, 3], 1:[0, 2, 3], 2:[0, 1, 3], 3:[0, 1, 2] }[correct_code]
            r = random.random() * 100
            if r <= 33:
               log = 'An incorrect answer with a code of ' + str(other_values[0]) + ' is given.  The correct code is ' + str(correct_code) + '.  First random number = ' + str(r1) + '.  Second random number = ' + str(r) 
               return [ other_values[0] , log ]
            if r <= 67:
               log = 'An incorrect answer with a code of ' + str(other_values[1]) + ' is given.  The correct code is ' + str(correct_code) + '.  First random number = ' + str(r1) + '.  Second random number = ' + str(r) 
               return [ other_values[1] , log ]
            log = 'An incorrect answer with a code of ' + str(other_values[2]) + ' is given.  The correct code is ' + str(correct_code) + '.  First random number = ' + str(r1) + '.  Second random number = ' + str(r)
            return [ other_values[2] , log ]

        def initialize_correct_answers(self,filePath,sheetName):
            """This keyword returns a dictionary with png_filename=key ,correct_answer=value"""
            workbook = xlrd.open_workbook(filePath)
            global CorrectAnswerDictionary
            CorrectAnswerDictionary = {}
            sheetName=str(sheetName)
            print sheetName
            worksheet=workbook.sheet_by_name(sheetName)
            noofrows=worksheet.nrows
            print noofrows
            for rowno in range(0,noofrows):
                rowValues=worksheet.row_values(rowno)
                print rowno
                print rowValues
                CorrectAnswerDictionary[str(rowValues[0])]=str(rowValues[1])
            return CorrectAnswerDictionary               

        def initialize_students_test_data(self,filePath,sheetName):
            """ Reading the students data"""
            workbook = xlrd.open_workbook(filePath)
            sheetName=str(sheetName)
            print sheetName
            worksheet=workbook.sheet_by_name(sheetName)
            noofrows=worksheet.nrows
            studentsDictionary={}
            print noofrows
            for rowno in range(0,noofrows):
                rowValues=worksheet.row_values(rowno)
                print rowno
                print rowValues
                studentsDictionary[int(rowno)]=rowValues
            return studentsDictionary               
            
            
                                
