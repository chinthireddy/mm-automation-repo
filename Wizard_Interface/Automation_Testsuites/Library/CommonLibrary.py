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
from random import randint
from urllib2 import Request, urlopen, URLError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from sys import exit
from httplib2 import Http
from urllib import urlencode
import httplib2
import pycurl
import certifi
import StringIO

class CommonLibrary:

        def __init__(self):
                pass
        def get_chrome_browser_options(self):
            """ This keyword will return chrome options """ 
            dictionary= {'profile.default_content_settings.popups':'0'} 
            chrome_options = Options()
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("test-type")            
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options=chrome_options
            return chrome_options
        #Mys - 6246 : Update te_keys request to use authentication credentials.
        def get_Teacher_Code(self, sURL, sDBName, DBUserName, DBPassword):
            response = StringIO.StringIO() 
            curl = pycurl.Curl()
            curl.setopt(pycurl.CAINFO, certifi.where())
            curl.setopt(pycurl.URL, "https://"+str(DBUserName)+":"+str(DBPassword)+"@"+str(sURL)+"/"+str(sDBName)+"/_design/te_keys/_update/generate/")
            curl.setopt(curl.WRITEFUNCTION, response.write)
            curl.setopt(curl.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
            curl.setopt(curl.POSTFIELDS, '@request.json')
            curl.perform()
            print response.getvalue()
            tecode = response.getvalue()
            return response.getvalue()
        #Mys - 5313 : Following keyword has built inorder to request a new TE_Code creation and return it to use it in registration process for current test URL/DB.
        def get_TE_Code(self, sURL, sDBName):
            conn = httplib2.Http()
            resp, resp_body = conn.request("http://"+str(sURL)+":80/"+str(sDBName)+"/_design/te_keys/_update/generate", "POST")
            #print resp_body
            if str(resp).find('201'):
                    return resp_body
            else:
                     raise AssertionError('Unable to Fetch TE code from URL : '+str(sURL)+' and Data Base : '+str(sDBName)+' => response Code is : '+str(resp))
        
        def click_element_using_javascript(self,locator,n=1):
                    """Returns 'True' if the element clciking by Java Script with the 'locator' in the corresponding page else returns 'False' """

                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        elements = selenium._element_find(locator,False,True)
                        selenium._current_browser().execute_script("arguments[0].click();", elements[n-1])
                        return True
                    except Exception as exp:
                        print "not clcikable by JS, "+ str(exp)
                        return False

        def capture_page_screenshot_and_log(self, out_folder, screenshot_name=None):
            """ take a screen shot and log browser, driver and server entries """
            out_folder = out_folder or '.'
            if screenshot_name==None:
                    screenshot_name="Screenshots"+self.get_unique_id()+".png"             
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium.capture_page_screenshot(filename=screenshot_name)
            status = self.capture_console_log(out_folder)
            return status
                        
        def Capture_whole_screen_and_log(self, out_folder, screenshot_name="Screenshots"):
            """ take entire window screen shot and log browser, driver and server entries """
            out_folder = out_folder or '.'
            secreenshot = BuiltIn().get_library_instance('Screenshot')
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            secreenshot.take_screenshot(out_folder + os.path.sep + screenshot_name)        
            status = self.capture_console_log(out_folder)
            return status

        def capture_console_log(self,out_folder):
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            browser = selenium._current_browser()
            print browser.name
           # ONLY FOR CHROME: log new browser console and driver entries if environment variable is not 'OFF'
            log_level = os.getenv('SELENIUM_LOG_LEVEL', 'OFF')
            if browser.name == 'chrome' and log_level != 'OFF':
                try:
                    with open(out_folder + os.path.sep + "browser.log", "a+") as data:
                        entries = selenium._current_browser().get_log('browser')
                        print "entries"
                        print entries
                        for entry in entries:
                            data.write(str(entry) + os.linesep)
                except:
                    print 'failed to append to browser.log file'
                try:
                    with open(out_folder + os.path.sep + "driver.log", "a+") as data:
                        entries = selenium._current_browser().get_log('driver')
                        for entry in entries:
                            data.write(str(entry) + os.linesep)
                except:
                    print 'failed to append to driver.log file'
            return True   


        def get_unique_id(self):
            """Returns Unique Value by adding Time Stamp"""
            #MYS-2512_Get_Unique_Values_Fix : Updated code to to get unique names based on timestamp with random number generation(to over come failures of test scripts run in parallel on same DB. )
            return 'sdt'+str(time.localtime().tm_year)+str(time.localtime().tm_mon)+str(time.localtime().tm_mday)+str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec)+str(int(round(time.time() * 1000)))[-4:] + str(random.randint(int(0000),int(9999)))

        def get_time_stamp(self):
            """Returns the Current Date and Time
            """
            return datetime.datetime.now(est()).strftime('%a %m/%d/%Y %I:%M %p')

        def close_alert_message(self):
            """Returns 'True'if any alert message displayed returns 'False' if not"""
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            try:
                selenium.get_alert_message()
                return True
            except:
                return False

        def type_of_variable(self,variable):
            """ check the type of given variable """
            varType = str(type(variable))
            varType = varType.replace("'","").replace(">","").replace("<","")
            tempList = varType.split(" ")
            return tempList[1]
        
        def get_alert_message(self):
            """Returns 'True' and 'Alert Text'in alert message if not returns 'False' and empty"""
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            text = ''
            try:
                text=selenium.get_alert_message()
                return [True,text]
            except:
                return [False,text]
            
        def verify_element_present(self,locator):
            """Returns 'True' if the element found with the 'locator' in the corresponding page else returns 'False'
            """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            bStatus = selenium._is_element_present(locator)
            if bStatus != True:
                    selenium.capture_page_screenshot()                    
            return bStatus

        def verify_element_visible(self,locator):
            """ Returns 'True' if the element visible with the 'locator' in the corresponding page else returns 'False' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            #Updated code to handle stale element kind of exceptions and to return a staus value.  
            try:
                    bStatus = selenium._is_visible(locator)
            #MYS-3191:Removed specific exception statement in block,inorder to handle all kind of exceptions.
            except:
                    bStatus= False
            if bStatus !=True:
                    selenium.capture_page_screenshot()
            return bStatus

        def is_digit(self,string):
            return string.isdigit()

        def list_comparison(self, li_actual, li_expected,message=''):
            """ Takes Two lists as Arguments and Pass if the two lists are equal else Fails"""
            print 'Expected: %s\n' % str(li_expected)
            print 'Actual: %s' % str(li_actual)
            if li_actual == []:
                raise AssertionError('Actual is empty')                    
            for index in range(0,len(li_expected)):
                if li_expected[index] in li_actual:
                    continue
                for actualIndex in range(0,len(li_actual)):
                    if li_expected[index][:14] in li_actual[actualIndex]:
                        break
                else:
                    raise AssertionError('Actual does not match expected'+str(message))

        def get_element_index(self, table_locator,value):
            """Returns the index of the value located by the table locator 'table_locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            index = self._get_element_index(table_locator,value)
            return index

        def type_keys_into_textbox(self, text_locator,value):
            """Enters text 'value' into 'text_locator' after checking the presence of the locator"""
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(text_locator,True,True).send_keys(value)
        def mouse_move(self, locator):
            """Moves the Mouse to the 'locator'"""
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium.mouse_over(locator)

        def wait_for_ajax(self,time_out=5):
            """ Wailt for given time"""
            '''selenium = BuiltIn().get_library_instance('Selenium2Library')
            status = selenium._selenium.get_eval('(window.jQuery || { active : 0 }).active')
            print status'''
            timeout = 0
            while(timeout<time_out):
                '''status = selenium._selenium.get_eval('(window.jQuery || { active : 0 }).active')
                if(status):
                    return True'''
                time.sleep(1)
                timeout=timeout+1
            return True
        def _get_element_index(self,locator,expected):
            """Returns index of the element at which the 'expected' value found """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            elements = selenium.get_matching_xpath_count(locator)
            for ele in range(int(elements)):
                newelements = selenium._element_find(locator,False,False)
                actual = newelements[ele].text
                if expected in actual:
                    print "header:"+str(newelements[ele].text)
                    print 'matched at'+str(ele+1)
                    return ele+1
            else:
                return 0
        def select_my_window(self,windowname=''):
            """Selects the window by the window name """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            browser = selenium._current_browser()
            #print browser.get_current_window_info()
            x=browser.get_window_handles()
            print x
            '''if windowname=='':
                browser.switch_to_window(x[0])'''
            browser.switch_to_window(x[1])
            print 'done'
            '''for handle in range(len(x)):
                browser.switch_to_window(x[handle])
                print selenium.get_title()'''
            return True

        def press_down_key(self,locator):
            """ Presses the down Key starting from the 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(locator,True,True).send_keys(Keys.ARROW_DOWN)

        def press_up_key(self,locator):
            """ Presses the up Key starting from the 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(locator,True,True).send_keys(Keys.ARROW_UP)              

        def get_items_in_context_menu(self, locator):
            """Returns the text from the context menu located by 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            return selenium.execute_javascript("return document.getElementById('dashMenu_4').getElementsByTagName'div')[1].getElementsByClassName('rich-menu-item rich-menu-item-enabled')["+str(locator)+"].getElementsByTagName('span')[1].textContent")

        def get_element_text(self,element,child):
            """Returns the text found at the 'child' of the 'element' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            id = selenium.get_element_attribute(element+'@id')
            print "id:"+str(id)
            return selenium.execute_javascript('return document.getElementById("'+id+'").childNodes['+str(child)+'].textContent')
            #return selenium.execute_javascript("return document.getElementById('"+id+"').childNodes['"+str(child)+"'][2].getElementsByTagName('td').textContent")

        def input_file_name(self,locator,value):
            """Enters the 'value' into the field located by 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(locator,True,True).send_keys(value)
            return True

        def get_current_date(self):
            """ Returns the current date in the format month date year"""
            cdate = datetime.datetime.now()
            return cdate.strftime("%m/%d/%Y")

        def get_future_or_past_date_from_now(self,noofdays=1):
            """Returns future(+days) / past(-days) date based on the given number of days(for past date give -ve integer for no of days)"""
            cdate = datetime.datetime.now()
            frpdate = cdate + datetime.timedelta(int(noofdays))
            frpdate = frpdate.strftime("%m/%d/%Y")
            return frpdate

        def delete_space(self,word):
            """deletes an undesired spce from the 'word' and returns the word """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            words = str(word)
            deletespace = words.replace(' ','')
            return deletespace
            
        def change_date_format(self, date):
            """ Returns a date after changing its format from 'month/date/year' to 'Year month date'"""
            #date = date.replace('/',",")
            return datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y,%m,%d')

        def compare_dates_for_given_range(self, date1, date2):
            """ Returns True if the 'date1' is less than 'date2' else fails"""
            date1 = self.change_date_format(str(date1))
            date2 = self.change_date_format(str(date2))
            return datetime.date(date1)<datetime.date(date2)
        def list_comp_by_sequence(self, actualList,expectedList):
            """Takes lists 'actualList' and 'expectedList'as arguments and compares them in the sequence """
            if cmp(actualList,expectedList)!=0:
                return False
            return True
        def get_length_of_list(self, actuallist):
            """Takes the list 'actuallist' as argument and finds the length of the list. Fails if the length of the list equal to Zero""" 
            if len(actuallist)==0:
                raise AssertionError('Actual is empty')
            return len(actuallist)
        def clear_text(self,locator):
            """Clears Text From the field located by 'locator'"""
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(locator,True,True).clear()
          
        def select_window_by_title(self,windowtitle):
            """Select a window by window title"""
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            #browser = selenium._current_browser()
            windows=selenium.get_window_titles()
            for window in windows:
                if window==windowtitle:
                    selenium.select_window(window)                          

        def string_should_contain(self,string,substring):
            """Returns True if The string contains substring else False' """
            ind=string.find(substring)
            if ind>=0:
                return True
            return False

        def click_on_element(self,locator,msg=''):
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            #bStatus = selenium.wait_until_element_is_visible(locator,5,msg)
            self.mouse_move(locator)
            selenium.focus(locator)
            selenium.click_element(locator)
            #if bStatus != False:
             #      selenium.maximize_browser_window()
             #      time.sleep(2)
             #      self.mouse_move(locator)
             #      selenium.focus(locator)
             #      selenium.click_element(locator)
             #      return True
            #else:
             #      return False      

        def click_assignment_navigation_controller_buttons(self,operation_name,msg=''):
            """Clicks the buttons of assignment navigation controllers"""
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            #MYS-3211:Removed "Selenium2Library" reference and updated to call custom method from CommonLibrary.
            bStatus = self.wait_for_element_visible('//li[@id="navBtn'+str(operation_name)+'"]/div[@class="mblTabBarButtonIconArea"]/parent::li',30,msg)
            if bStatus != False:
                    selenium.maximize_browser_window()
                    time.sleep(10)
                    self.mouse_move('//li[@id="navBtn'+str(operation_name)+'"]/div[@class="mblTabBarButtonIconArea"]/parent::li')
                    selenium.focus('//li[@id="navBtn'+str(operation_name)+'"]/div[@class="mblTabBarButtonIconArea"]/parent::li')
                    #MYS-3211:Removed "Selenium2Library" reference and updated to call its robotframework method from BuiltIn Library.
                    BuiltIn().wait_until_keyword_succeeds('2m','5s','Selenium2Library.click_element',"//li[@id='navBtn"+str(operation_name)+"']/div[@class='mblTabBarButtonIconArea']/parent::li")
                    return True
            else:
                    return False

        def press_enter_key(self,locator):
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            self.mouse_move(locator)
            selenium.focus(locator)
            selenium._element_find(locator,True,True).send_keys(Keys.ENTER)

        def press_control_and_key(self,locator,key):
            """Presses the control Key and Specified key 'key' at element located by the 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            loc = selenium._element_find(locator,True,True)
            loc.send_keys(Keys.CONTROL, 'a')
            time.sleep(1)
            loc.send_keys(Keys.CONTROL,key)
            time.sleep(1)
            
        def press_right_key(self,locator):
            """Presses the Right Key at element located by the 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(locator,True,True).send_keys(Keys.ARROW_RIGHT)

        def press_page_down_key(self,locator):
            """Presses the page down Key starting from the 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(locator,True,True).send_keys(Keys.PAGE_DOWN)

        def press_page_up_key(self,locator):
            """Presses the page up Key starting from the 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(locator,True,True).send_keys(Keys.PAGE_UP)

        def press_home_key(self,locator):
            """Presses the Home Key starting from the 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(locator,True,True).send_keys(Keys.HOME)

        def press_end_key(self,locator):
            """Presses the End Key starting from the 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(locator,True,True).send_keys(Keys.END)


        def is_list_contains_value(self,statuslist,value):
            """ checks the given value in the list """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            statuslistvalues = []
            statuslistvalues = statuslist
            return value in statuslistvalues

        def get_random_number_in_given_range(self,start,stop):
            """ Returns the random from given range"""
            return random.randint(int(start),int(stop))

        def convert_string_case(self,string,case=''):
            """Converts the Case of the string to Upper if specified else to lower """
            if case=="upper":
                return string.upper()
            else:
                return string.lower()
            
        def table_get_column_no(self, table_locator, columnName):
            """Returns the column number of the column matching 'columnName' from the table located at 'table_locator'."""
            #try:
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium.wait_until_element_is_visible(table_locator,time.sleep(10))
            colCount = int(selenium.get_matching_xpath_count(table_locator+'/div[contains(@class,"dgrid-header dgrid-header-row")]/table[contains(@id,"-header")]/tr/th'))
            print "colCount:"+str(colCount)
            for iCounter in range(1,colCount+1):
                curColName = selenium._get_text(table_locator+'//div[contains(@class,"dgrid-header dgrid-header-row")]/table[contains(@id,"-header")]/tr/th['+str(iCounter)+']')
                if (curColName.replace(' ','').strip().lower()==columnName.replace(' ','').strip().lower()):
                    print "column name matched at "+str(iCounter)
                    return iCounter
            return 0

        def get_table_values_into_list(self, locator, columnName):
            """Returns the list of values displayed under 'columnName' from the table located at 'locator' """
            print "locator:" + str(locator)
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            #Get the column number
            iColNo = self.table_get_column_no(locator,columnName)
            #Get the Number of Records in the Table
            elements = selenium.get_matching_xpath_count(locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]')
            print "elements:"+str(elements)
            rowValues = []
            #Get the values from the records
            for ele in range(1,int(elements)+1):
                cellValue = selenium._get_text(locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]['+str(ele)+']/table/tr/td[contains(@class,"dgrid-cell")]['+str(iColNo)+']')
                rowValues.append(cellValue)
            return rowValues
        def verify_values_in_table(self, locator, columnName,value,sortingStatus=True):
            """Returns the list of values displayed under 'columnName' from the table located at 'locator' """
            print "locator:" + str(locator)
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            if sortingStatus == True:
                    self.table_column_values_sorting(locator, 'Created','descend')
            #Get the column number
            iColNo = self.table_get_column_no(locator,columnName)
            #Get the Number of Records in the Table
            elements = selenium.get_matching_xpath_count(locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]')
            print "elements:"+str(elements)
            rowValues = []
            #Get the values from the records
            for ele in range(1,int(elements)+1):
                cellValue = selenium._get_text(locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]['+str(ele)+']/table/tr/td[contains(@class,"dgrid-cell")]['+str(iColNo)+']')
                if (value == cellValue):
                        return True        
            return False
        def select_the_record_in_table(self, locator, columnName,value,sortingStatus=True):
            """Returns the row number of specifed value under 'columnName' from the table located at 'locator' """
            print "locator:" + str(locator)
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            if sortingStatus == True:
                    self.table_column_values_sorting(locator, 'Created','descend')
            #Get the column number
            iColNo = self.table_get_column_no(locator,columnName)
            #Get the Number of Records in the Table
            elements = selenium.get_matching_xpath_count(locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]')
            print "elements:"+str(elements)
            rowValues = []
            #Get the values from the records
            for ele in range(1,int(elements)+1):
                cellValue = selenium._get_text(locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]['+str(ele)+']/table/tr/td[contains(@class,"dgrid-cell")]['+str(iColNo)+']')
                print "cellValue: "+str(cellValue)
                if (value == cellValue):
                        selenium.click_element(locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]['+str(ele)+']/table/tr/td[contains(@class,"dgrid-cell")]')
                        return ele
            return 0

        def table_column_values_sorting(self, locator, columnName,sortorder='descend'):
            """ Keyword is used to column sorting based on table and column value."""
            print "locator:" + str(locator)
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            #verify the table
            try:
                selenium.wait_until_element_is_visible(locator,"30s")
            except:
                print "Table was not dispayed"
            #Get the column number
            iColNo = self.table_get_column_no(locator,columnName)
            if iColNo == 0:
                return False
            #updated code for MYS-2566 to handle DOM exception while sorting table based on given colummn name.
            for iCounter in range(1,5):
                    try:
                            print "tryblock"+ str(iCounter)
                            selenium.click_element(locator+"/div[contains(@class,'dgrid-header-rowmmmm')]/table/tr/th[text()='"+str(columnName)+"']")
                            break
                            
                    except:
                            print "catchblock"+ str(iCounter)
            #selenium.click_element(locator+"/div[contains(@class,'dgrid-header-row')]/table/tr/th[text()='"+str(columnName)+"']")
            for iCounter in range(1,5):
                time.sleep(1)
                print "iCounter: "+str(iCounter)
                selenium.click_element(locator+"/div[contains(@class,'dgrid-header-row')]/table/tr/th[text()='"+str(columnName)+"']")
                time.sleep(2)
                columnClassStatus = self.verify_element_visible(locator+"/div[contains(@class,'dgrid-header-row')]/table/tr/th[text()='"+str(columnName)+"' and contains(@class,'dgrid-sort-down')]")
                print "columnClassStatus: "+str(columnClassStatus)
                sortStatus = self.string_should_contain(sortorder,'descend')
                print "sortStatus: "+str(sortStatus)
                if (columnClassStatus == True and sortStatus == True) or (columnClassStatus != True and sortStatus == False):
                    return True
            selenium.capture_page_screenshot()
            return False

        def get_table_cell_value(self, table_locator, rowNo,colName):
            "Returns the text located in the table 'table_locator' with in the Column 'columnName' and matching Row 'iRowNo'"""
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            colNo=self.table_get_column_no(table_locator,colName)
            return selenium._get_text(table_locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]['+str(rowNo)+']/table/tr/td[contains(@class,"dgrid-cell")]['+str(colNo)+']')
        def select_the_row(self, table_locator, rowNo):
            "Returns the text located in the table 'table_locator' with in the Column 'columnName' and matching Row 'iRowNo'"""
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            #MYS-3105 : Updated with "wait for element visible" keyword to handle DOM exceptions.
            self.wait_for_element_visible(table_locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]['+str(rowNo)+']')
            return selenium.click_element(table_locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]['+str(rowNo)+']')



        def validate_the_sheet_in_ms_excel_file(self,filepath,sheetName):
            """Returns the True if the specified work sheets exist in the specifed MS Excel file else False"""
            workbook = xlrd.open_workbook(filepath)
            snames=workbook.sheet_names()
            sStatus=False        
            if sheetName==None:
                return True
            else:
                for sname in snames:
                    if sname.lower()==sheetName.lower():
                        wsname=sname
                        sStatus=True
                        break
                if sStatus==False:
                    print "Error: The specified sheet: "+str(sheetName)+" doesn't exist in the specified file: "+str(filepath)
            return sStatus


        def get_ms_excel_file_rows_count(self,filepath,sheetName=None):
            """Return The Total No Rows In MS Excel File Using The Specified File filepath"""
            workbook = xlrd.open_workbook(filepath)
            snames=workbook.sheet_names()
            if sheetName==None:
                sheetName=snames[0]      
            if self.validate_the_sheet_in_ms_excel_file(filepath,sheetName)==False:
                return -1
            worksheet=workbook.sheet_by_name(sheetName)
            return worksheet.nrows


        def get_ms_excel_row_values_into_list(self,filepath,rowNumber,sheetName=None):
            """Returns the list of values given row in the MS Excel file """
            workbook = xlrd.open_workbook(filepath)
            snames=workbook.sheet_names()
            tempList=[]
            if sheetName==None:
                sheetName=snames[0]      
            if self.validate_the_sheet_in_ms_excel_file(filepath,sheetName)==False:
                return tempList
            worksheet=workbook.sheet_by_name(sheetName)
            noofrows=worksheet.nrows
            tempList=[]
            for rowno in range(0,noofrows):
                row=worksheet.row(rowno)
                for colno in range(0,len(row)):
                    cellval=worksheet.cell_value(rowno,colno)
                    if int(rowNumber)==int(int(rowno)+1):
                        tempList.append(cellval)
            return tempList
            


        def get_ms_excel_column_values_into_list(self,filepath,colNumber,sheetName=None):
            """Returns the list of values given column in the MS Excel file """
            workbook = xlrd.open_workbook(filepath)
            snames=workbook.sheet_names()
            tempList=[]
            if sheetName==None:
                sheetName=snames[0]      
            if self.validate_the_sheet_in_ms_excel_file(filepath,sheetName)==False:
                return tempList
            worksheet=workbook.sheet_by_name(sheetName)
            noofrows=worksheet.nrows
            #print "No.of Rows:" +str(noofrows)
            tempList=[]
            for rowno in range(1,noofrows):
                row=worksheet.row(rowno)
                for colno in range(0,len(row)):
                    cellval=worksheet.cell_value(rowno,colno)
                    if int(colNumber)==int(int(colno)+1):
                        tempList.append(cellval)
            #print "Last Value:" +str(cellval)
            tempList = [str(x) for x in tempList]
            return tempList

        def press_back_space_key(self,locator):
            """ Presses the down Key starting from the 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(locator,True,True).send_keys(Keys.BACK_SPACE)


        def press_space_key(self,locator):
            """ Presses the space Key starting from the 'locator' """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            selenium._element_find(locator,True,True).send_keys(Keys.SPACE)

        def get_ms_excel_row_values_into_dictionary(self,filepath,rowNumber,sheetName=None):
            """Returns the dictionary of values given row in the MS Excel file """
            workbook = xlrd.open_workbook(filepath)
            snames=workbook.sheet_names()
            dictVar={}
            if sheetName==None:
                sheetName=snames[0]      
            if self.validate_the_sheet_in_ms_excel_file(filepath,sheetName)==False:
                return dictVar
            worksheet=workbook.sheet_by_name(sheetName)
            noofrows=worksheet.nrows
            dictVar={}
            headersList=worksheet.row_values(int(0))
            print 'headersList'
            print headersList
            rowValues=worksheet.row_values(int(rowNumber)+1)
            for rowIndex in range(0,len(rowValues)):
                dictVar[str(headersList[rowIndex])]=str(rowValues[rowIndex])
            return dictVar

        def get_ms_excel_row_values_into_dictionary_based_on_key(self,filepath,keyName,sheetName=None):
            """Returns the dictionary of values given row in the MS Excel file """
            workbook = xlrd.open_workbook(filepath)
            snames=workbook.sheet_names()
            dictVar={}
            if sheetName==None:
                sheetName=snames[0]      
            if self.validate_the_sheet_in_ms_excel_file(filepath,sheetName)==False:
                return dictVar
            worksheet=workbook.sheet_by_name(sheetName)
            noofrows=worksheet.nrows
            dictVar={}
            headersList=worksheet.row_values(int(0))
            for rowNo in range(1,int(noofrows)):
                rowValues=worksheet.row_values(int(rowNo))
                if str(rowValues[0])!=str(keyName):
                    continue
                for rowIndex in range(0,len(rowValues)):
                    cell_data=rowValues[rowIndex]
                    cell_data=self.get_unique_test_data(cell_data)
                
                    dictVar[str(headersList[rowIndex])]=str(cell_data)
            return dictVar

        def get_unique_test_data(self,testdata):
            """Returns the unique if data contains unique word """
            testdata=str(testdata)
            timestamp=self.get_current_time_stamp(False)
            testdata=testdata.replace("unique",timestamp)
            testdata=testdata.replace("Unique",timestamp)
            return testdata

        def get_current_time(self):
            """Return the Current date value"""
            return time.strftime("%H-%M-%S")

        def get_current_time_stamp(self,bStatus=True):
            """Return the Current date value"""
            ts=datetime.datetime.now()
            if bStatus==True:
                    ts=(str(ts).split(".")[0]).replace("-","").replace(":","").replace(" ","")
            else:
                    ts=(str(ts).split(" ")[1]).replace(".","").replace(":","")
                    n=randint(1,99)
                    ts=str(ts)+str(n)
            return ts


        def create_csv_file_using_ms_excel_file(self,csvfilepath,excelfilepath,sheetName=None):
            """Returns the row number of the given text in the MS Excel file """
            workbook = xlrd.open_workbook(excelfilepath)
            snames=workbook.sheet_names()
            opFile=open(str(csvfilepath), "wb");
            writer = csv.writer(opFile)
            tList=[]
            if sheetName==None:
                sheetName=snames[0]      
            if self.validate_the_sheet_in_ms_excel_file(excelfilepath,sheetName)==False:
                return -1
            worksheet=workbook.sheet_by_name(sheetName)
            noofrows=worksheet.nrows
            headersList=[]
            for rowno in range(0,noofrows):
                tempList=[]
                dictVar={}
                rowValues=worksheet.row_values(rowno)
                rowValues = [str(x) for x in rowValues]
                if rowno==0:
                     headersList=rowValues
                for ind in range(0,len(rowValues)):
                        val=self.get_unique_test_data(rowValues[ind])
                        tempList.append(val)
                        if rowno!=0:
                                dictVar[str(headersList[ind])]=str(val)
                tempList.remove(str(tempList[0]))
                writer.writerow(tempList)
                if rowno!=0:
                        tList.append(dictVar)
            opFile.close()
            return tList

        def prepare_students_details_csv_by_adding_additional_columns(self,csvfilepath,excelfilepath,columnName1,list1,columnName2,list2,sheetName=None):
            """Creates student details csv for uploading by adding some additional columns"""
            workbook = xlrd.open_workbook(excelfilepath)
            snames=workbook.sheet_names()
            opFile=open(str(csvfilepath), "wb");
            writer = csv.writer(opFile)
            tList=[]
            if sheetName==None:
                sheetName=snames[0]      
            if self.validate_the_sheet_in_ms_excel_file(excelfilepath,sheetName)==False:
                return -1
            worksheet=workbook.sheet_by_name(sheetName)
            noofrows=worksheet.nrows
            headersList=[]
            for rowno in range(0,noofrows):
                tempList=[]
                dictVar={}
                rowValues=worksheet.row_values(rowno)
                rowValues = [str(x) for x in rowValues]
                if rowno==0:
                        rowValues.append(str(columnName1))
                        rowValues.append(str(columnName2))
                else :
                        rowValues.append(list1[int(rowno)-1])
                        rowValues.append(list2[int(rowno)-1])
                if rowno==0:
                     headersList=rowValues
                for ind in range(0,len(rowValues)):
                        val = str(rowValues[ind])
                        tempList.append(val)
                        if rowno!=0:
                                dictVar[str(headersList[ind])]=str(val)        
                tempList.remove(str(tempList[0]))
                writer.writerow(tempList)
                if rowno!=0:
                        tList.append(dictVar)
            opFile.close()
            return tList

        def get_csv_file_column_values_into_list(self,path,columnname):
            """Returns the list of specified columns values from cvs file in Specified File by 'path' """
            keyColno=self.get_csv_file_column_no(path,columnname)
            print 'keyColno:'+str(keyColno)
            file_Reader = csv.reader(open(path))
            rowNumber=0
            lines=[]
            columnValues=[]
            keyColno=int(keyColno)-1
            for row in file_Reader:
                rowNumber=rowNumber+1
                columnValues.append(row[keyColno])
            return columnValues

        def get_csv_file_column_no(self,path,columnname):
            """Returns the column of specified column by  columnname from cvs file in Specified File by 'path' """
            file_Reader = csv.reader(open(path))
            linevalues=[]
            for row in file_Reader:
                linevalues=row
                break
            for index in range(0,len(linevalues)):
                if linevalues[index]==columnname:
                    return index+1
            return 0
        def get_csv_file_row_values_into_list(self,path,rowNo):
            """Returns the list of specified row values from cvs file in Specified File by 'path' """
            file_Reader = csv.reader(open(path))
            rowNumber=0
            lines=[]
            for row in file_Reader:
                rowNumber=rowNumber+1
                if rowNumber==int(rowNo):
                    lines=row
                    break
            return lines

        def get_csv_file_column_values_into_list_by_columnindex(self,path,columnindex):
            """Returns the list of specified columns values from cvs file in Specified File by 'path' using columnindex number"""
            print 'columnindex:'+str(columnindex)
            file_Reader = csv.reader(open(path))
            rowNumber=0
            lines=[]
            columnValues=[]
            columnindex=int(columnindex)-1
            for row in file_Reader:
                rowNumber=rowNumber+1
                columnValues.append(row[columnindex])
            return columnValues
        
        def get_zipcode_for_school(self,filePath,sheetName,schoolName):
            """"Return the zipcode based school name"""
            zipCode = ""
            workbook = xlrd.open_workbook(filePath)
            schoolName=str(schoolName)
            worksheet = workbook.sheet_by_name(sheetName)
            noofrows = worksheet.nrows
            headersList = self.get_ms_excel_row_values_into_list(filePath,int(1),sheetName)
            colIndex = headersList.index(schoolName)
            columnIndex = int(colIndex)+1
            columnValues = self.get_ms_excel_column_values_into_list(filePath,columnIndex,sheetName)
            zipCode = str(columnValues[0])
            tempList = zipCode.split("Zip: ")
            zipCode = tempList[1]
            return zipCode
        def get_ms_excel_column_values_into_list_by_column_name(self,filePath,sheetName,columnName):
            """ It retuen the list of registration codes"""
            workbook = xlrd.open_workbook(filePath)
            columnName=str(columnName)
            worksheet = workbook.sheet_by_name(sheetName)
            noofrows = worksheet.nrows
            headersList = self.get_ms_excel_row_values_into_list(filePath,int(1),sheetName)
            colIndex = headersList.index(columnName)
            columnIndex = int(colIndex)+1
            columnValues = []
            for rowNo in range(1,int(noofrows)):
                rowValues=worksheet.row_values(int(rowNo))
                columnValues.append(rowValues[colIndex])
            return columnValues
        
        def wait_for_web_app_loading_progress(self,locator,timeout):
            """ Keyword is used to wait for a loadingProgressMoniotor with tiny green progress bar. """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            try:
                for index in range(1,5):
                    print "index:"+str(index)+" done"
                    try:
                        selenium.wait_until_element_is_visible(locator,timeout)
                    except:
                        print "Green Progress Bar Not Visible"
                        time.sleep(5)
                    bStatus = self.verify_element_visible(locator)
                    print bStatus
                    if bStatus == True:
                        break
                    else:
                        selenium.reload_page()
                        print "Reloading the Page"
                        time.sleep(5)
                for iCounter in range(1,5000):
                        percentageText = selenium._get_text(locator)
                        print "percentageText:"+str(percentageText)
                        tempList = percentageText.split("%")
                        if len(tempList)== 1:
                           return False
                        percentageVal = tempList[0]
                        print "percentageVal:"+str(percentageVal)
                        time.sleep(1)
                        if float(percentageVal) > 0.9:
                           break
                return True
            except:
                return False

        def student_do_the_assignment(self,assignmentName,subTitle='',startStatus=True):
            """ this keyword Starts the assignment bydefault if "startStatus" given False it return Assignment Row index only with starting assignment"""
            locator = "//div[contains(@id,'studentAssmtGrid-row') and @role='row']"
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            try:
                selenium.wait_until_element_is_visible(locator,"30s")
            except:
                print "Assignments are not displayed"
            assignmentsCount = selenium.get_matching_xpath_count(locator)
            subTitleList = subTitle.split("(")
            subTitle = subTitleList[0].strip()
            print "assignmentsCount:"+str(assignmentsCount)
            for iCounter in range(1,int(assignmentsCount)+1):
                assignmentDeatils = selenium._get_text(locator+str("[")+str(iCounter)+str("]//table/tr/td[2]"))
                print "assignmentDeatils: "+str(assignmentDeatils)
                bStatus1 = self.string_should_contain(assignmentDeatils,assignmentName)
                bStatus2 = self.string_should_contain(assignmentDeatils,subTitle)
                if bStatus1==True and (subTitle == '' or bStatus2==True):
                    print "Assignment matched in row "+str(iCounter)
                    if startStatus == True:
                        selenium.click_element(locator+str("[")+str(iCounter)+str("]//table/tr/td[1]//div[contains(@class,'Button')]"))
                        try:
                            selenium.wait_until_element_is_visible(BuiltIn().get_variable_value("${button.studentAssignments.PauseButton}"),"30s")
                        except:
                            print "submit was not displayed"                
                    return iCounter
            selenium.capture_page_screenshot()
            return 0

        def verify_the_assignments_list(self):
            """ this keyword returns assignments list status True if any assignment exist otherwise False """
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            try:
                selenium.wait_until_element_is_visible(BuiltIn().get_variable_value("${table.StudentHome.AssignmentsRow}"),"30s")
                print "Assignments are displayed"
            except:
                print "Assignments are not displayed"
            assignmentsListStatus = self.verify_element_visible(BuiltIn().get_variable_value("${table.StudentHome.AssignmentsRow}"))
            print "assignmentsListStatus:"+str(assignmentsListStatus)
            noAssignmentsStatus = self.verify_element_visible(BuiltIn().get_variable_value("${label.StudentHome.No Assignments}"))
            print "noAssignmentsStatus:"+str(noAssignmentsStatus)
            if (assignmentsListStatus == True and str(noAssignmentsStatus) != 'True'):
                return True
            return False
                
        def create_csv_file_using_dictionary_values(self,csvfilepath,twoDimDictionary):
            """Creates a csv file in the given csvfilepath with twodimdictionary data"""
            kwStatus = False;
            opFile=open(str(csvfilepath), "wb");
            writer = csv.writer(opFile)
            keys = twoDimDictionary.keys()
            print keys
            noOfStudDetails = len(keys)
            for stud in range (0,int(noOfStudDetails)):
                    studentDetails = twoDimDictionary[keys[stud]]
                    rowValues = studentDetails.values()
                    if int(stud)==0:
                            headersList = studentDetails.keys()
                            writer.writerow(headersList)
                    writer.writerow(rowValues)
                    kwStatus = True
            opFile.close()
            return kwStatus

        def get_assignment_progress(self,assignmentName,subTitle):
            """ It returns the Assignment Progress value based on Title and Activity Names"""
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            assignmentRowNo = self.student_do_the_assignment(assignmentName,subTitle,False)
            if assignmentRowNo ==0:
                    return -1
            assignmentsprogress = selenium._get_text(BuiltIn().get_variable_value("${table.StudentHome.AssignmentsRow}")+"["+str(assignmentRowNo)+"]"+BuiltIn().get_variable_value("${label.StudentHome.AssignmentProgrss}"))
            return assignmentsprogress

        def get_teacher_registration_code(self, codes_url):
            """it returns the list of registration codes which can be used during teacher signup"""
            RegCode = BuiltIn().run_keyword("common.Get_TE_Code_For_Current_Test_URL")
            #Mys - 5313 : Following keyword code has been commented and modified as a part of new process of reading TE_Codes.
            """if not codes_url:
                raise ValueError('codes_url is empty')
            request = Request(codes_url)
            response = urlopen(request)
            PageSource = response.read()
            tempValues = PageSource.split('body')
            temp = tempValues[1].split('>',1)
            tempCodes = temp[1].split('</')
            RegCodes = tempCodes[0].split('<br>')
            RegCodes.remove("")
            iRandomIndex = random.randint(int(0),int(len(RegCodes)-1))
            RegCode = RegCodes[iRandomIndex]
            print 'Teacher Reg Code: '+ str(RegCode)"""
            return RegCode

        def get_school_instructions_from_url(self):
            """It returns all the data described in the URL"""
            """ use either request = Request('http://v4.tomo.zone/mysdb_m3_sales/_design/mysPublisher/_list/process/sandbox') """
            """ or request = Request('http://b11test2a.mentoringmindsonline.com/mysdb_m3_test2/_design/mysPublisher/_list/process/sandbox') """
            request = Request('http://v4.tomo.zone/mysdb_m3_sales/_design/mysPublisher/_list/process/sandbox')
            response = urlopen(request)
            PageSource = response.read()
            for char in '\r\n':
                PageSource = PageSource.replace(char,'')
            return PageSource

        def get_matched_row_values_from_table(self, locator, columnName,value,sortingStatus=True):
            """Returns the list of row values displayed under 'columnName' where the column value macthing in the table located at 'locator' """
            print "locator:" + str(locator)
            selenium = BuiltIn().get_library_instance('Selenium2Library')
            if sortingStatus == True:
                    self.table_column_values_sorting(locator, 'Created','descend')
            #Get the column number
            iColNo = self.table_get_column_no(locator,columnName)
            #Get the Number of Records in the Table
            elements = selenium.get_matching_xpath_count(locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]')
            print "elements:"+str(elements)
            dctRowValues = {}
            #Get the values from the records
            for ele in range(1,int(elements)+1):
                cellValue = selenium._get_text(locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]['+str(ele)+']/table/tr/td[contains(@class,"dgrid-cell")]['+str(iColNo)+']')
                if (value == cellValue):
                        selenium.click_element(locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]['+str(ele)+']/table/tr/td[contains(@class,"dgrid-cell")]')
                        colmnsCount = selenium.get_matching_xpath_count(locator+"//div[contains(@class,'header-row')]/table/tr/th")
                        for indexVal in range(1,int(colmnsCount)+1):
                            colmName = selenium._get_text(locator+"//div[contains(@class,'header-row')]/table/tr/th["+str(indexVal)+"]")
                            colmValue = selenium._get_text(locator+'/div[@class="dgrid-scroller"]/div[contains(@class,"dgrid-content")]//div[contains(@id,"-row")]['+str(ele)+']/table/tr/td[contains(@class,"dgrid-cell")]['+str(indexVal)+']')
                            dctRowValues[colmName] = colmValue
            return dctRowValues
        
        def get_table_column_headers_into_list(self,tableLocator):
                selenium = BuiltIn().get_library_instance('Selenium2Library')
                colCount = selenium.get_matching_xpath_count(tableLocator+"//div[contains(@class,'dgrid-header dgrid-header-row')]/table/tr/th")
                columnHeadersList = []
                for col in range(1,int(colCount)+1):
                        columnName = selenium.get_text(tableLocator+"//div[contains(@class,'dgrid-header dgrid-header-row')]/table/tr/th["+str(col)+"]")
                        columnHeadersList.append(columnName)
                return columnHeadersList
        
        def search_the_records(self,tableLocator,searchLocator,searchValue) :
                selenium = BuiltIn().get_library_instance('Selenium2Library')
                #common = BuiltIn().get_library_instance('CommonLibrary')
                collections = BuiltIn().get_library_instance('Collections')
                #MYS-3371 : Replaced with wait for element visible keyword.
                bStatus = self.wait_for_element_visible(searchLocator,'5s')
                if bStatus == False:
                        #MYS-3371 : fixed wrong referencing instance from 'selenium' to 'BuiltIn'.
                        BuiltIn().Fail('The search locator is not visible')
                selenium.input_text(searchLocator,searchValue)
                headersList = self.get_table_column_headers_into_list(tableLocator)
                headersCount = self.get_length_of_list(headersList)
                tableValues = []
                for ele in range(0,int(headersCount)):
                        colvals = self.get_table_values_into_list(tableLocator,str(headersList[ele]))
                        tableValues.append(colvals)
                noOfRecords = self.get_length_of_list(tableValues[-1])
                for val in range(0,int(noOfRecords)):
                        #tableRecord = []
                        for col in range(0,int(headersCount)):
                                ColValue = tableValues[col][val]
                                #tableRecord.append(ColValue)
                                #collections.list_should_contain_value(tableRecord,searchValue,"The search values is not present in the displayed record of the table")
                                if (ColValue.find(searchValue) != -1 and col!=headersCount):
                                        break
                                else:
                                        if(col!=headersCount):
                                                continue
                                        else:
                                                return False
                return True

        def writeSchoolDetailsIntoTextFile(self,filePath,schoolDetailsDictionary):
            f = open(filePath, "w");
            dctKeys = schoolDetailsDictionary.keys()
            print dctKeys
            for dctKey in dctKeys:
                print dctKey
                dctVal = schoolDetailsDictionary[dctKey]
                f.write(str(dctKey) + " = "+str(dctVal))
                f.write("\n")
            f.close()
        
        # Designed a new keyword to handle DOM exceptions.
        def wait_for_element_visible(self,locator,timeout=None,message=''):
                    """Returns 'True' if the element visible with the 'locator' in the corresponding page else returns 'False' base timeout
                    """
                    #Update to handle errors with failure message text formatting for unknown ASCII characters included in parsed message.
                    message = message.encode('ascii','ignore')
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,3):
                        print "iCounter: "+str(iCounter)
                        try:
                            selenium.wait_until_page_contains_element(locator,timeout)
                            selenium.wait_until_element_is_visible(locator,timeout)
                            return True
                        except:
                            if(len(message)>0):
                                print "Error Message:" +str(message)
                            print "ValueError: Element locator "+str(locator) +" did not visible within "+str(timeout) +" time out"
                            print "locator: "+str(locator)
                    return False
