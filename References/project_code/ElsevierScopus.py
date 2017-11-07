#Needs to have a check functionality, if the data needs to be updated or not
#Put error catching clauses to some methods
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import urllib
import Importer as imp
import time
import datetime
import xlrd
import csv
import os

#!!!!Set the operating system before running this script following the example below!!!!
current_os="mac"
#current_os="linux"
#current_os="windows.exe"

#NOTES TO READER/USER
#Print ISSN and EISSN fields need to be string rather than int even though MysqlWorkbench automatically assigns int, because some values have characters in them.
#Empty values (in Elsevier indicated by "") need to be replaced by \N, to be type compatible with their respective fields, a bash script does this conversion.
#Elsevier data set has multiple sheets (for each year) when you download, to update the database you only need to get one before last sheet (last sheet is info not data).
#Elsevier webpage requires a form to be filled before accessing the download link, this class uses Selenium Webdriver to simulate form filling and post.
#After filling and posting the form, extractLinks method finds links that incldue .xlsx in the page and extracts to start downloading.
#Download method downloads all files found by extartLinks method, names them using source_name and filename_counter variables. Example: elsevier0.xlsx
#If any connection problems occur and page loading can not catch up with scripts pace (normally script should implicitly wait), set wait variable below to increase wait time while page loads.
wait=0

#Other variables
import_query = "LOAD DATA LOCAL INFILE 'ElsevierAuto/elsevier0_sheetLatest2.csv' INTO TABLE Elsevier FIELDS TERMINATED BY '\t' ENCLOSED BY '\"' ESCAPED BY '\\\\' IGNORE 1 LINES"
replace_empty_command= """awk 'BEGIN { FS = OFS = "\t" } { for(i=1; i<=NF; i++) if($i ~ /^ *$/) $i = "\N" }; 1's ElsevierAuto/elsevier0_sheetLatest.csv > ElsevierAuto/elsevier0_sheetLatest2.csv"""
starting_row=1 #For elsevier row 0 is description, no need


class ElsevierScopus:
        
        def __init__(self):
            self.source_name='ElsevierAuto/elsevier' #File will be saved under ElsevierAuto folder
            self.file_extension= '.xlsx'
            self.DOMAIN= 'scopus.com'
            self.URL= 'https://journalmetrics.scopus.com/'
            self.driver = webdriver.Chrome("./Chromedrivers/chromedriver_"+current_os)
            self.downloaded_file_path=self.source_name+str(0)
            self.converted_file_path=self.downloaded_file_path+"_sheetLatest.csv"
            self.download_links=[]
            self.update()
            
        def update(self): 
            print("Elsevier Scopus update is called.")
            self.scrape()
            self.Download()
            self.xlsToCsvLastSheet(self.downloaded_file_path, starting_row) #year must be current year -1, letting default value handle
            self.replaceEmptyNUll(self.converted_file_path)
            imp.Importer(import_query)
     
        def clickDownloadButton(self):
            self.driver.get(self.URL)
            element=self.driver.find_elements_by_xpath("//*[contains(text(), 'Download')]") #find elements containing 'Download'
            element[0].click() #click to the first element that containt Download
            print("Clicked to Download button.")
            self.waiter(wait)
            
        def fillForm(self):
             self.driver.find_element_by_id("recipient__firstName").send_keys("Alice")
             self.driver.find_element_by_id("recipient__lastName").send_keys("Banner")
             self.driver.find_element_by_id("recipient__email").send_keys("alicebanner@ymail.com")
             Select(self.driver.find_element_by_id("recipient__roleId")).select_by_visible_text("Student")
             self.driver.find_element_by_id("recipient__organization").send_keys("ULL")
             self.driver.find_element_by_id("submitButton").click()
             print("Submitted the form.")
             self.waiter(wait)
             
        def extractLinks(self):
            elems = self.driver.find_elements_by_xpath("//a[@href]")
            for elem in elems:
                if ".xlsx" in elem.get_attribute("href"): #can be extended with or .xls 
                    self.download_links.append(elem.get_attribute("href"))
            print("Extracted possible download links.")
        
        def scrape(self):
            self.driver.get_screenshot_as_png()
            self.clickDownloadButton()
            self.fillForm()
            self.extractLinks()
            return self.download_links
        
        def printLinks(self):
            print("Extracted download links from Scopus:")
            print(self.download_links)
            
        def Download(self):
            filename_counter=0
            for url in self.download_links:
                filename=self.source_name+str(filename_counter)+self.file_extension
                print("Downloading "+filename+"...")
                testfile = urllib.URLopener()
                testfile.retrieve(url, filename)
                filename_counter=filename_counter+1
                print("Downloading done.")
        
        def waiter(self, amount):
            time.sleep(amount)
            
        #Converts xlsx to tab separated CSV, method assumes starting row has the attribute names.
        #If not provided, year will be the current year-1 since most up to date data they provide is last year.
        def xlsToCsvLastSheet(self, filename, startingRow, year=datetime.date.today().year-1):
            print "XLS to CSV method is called for "+filename+", Last sheet, Year: "+str(year)
            with open(self.converted_file_path, 'wb') as myCsvfile:
                wr=csv.writer(myCsvfile, delimiter="\t")
                myfile=xlrd.open_workbook(filename+'.xlsx', 'rU')
                mysheet=myfile.sheet_by_index(len(myfile.sheets())-2) #get the given sheet
                print("Writing started.")
                for rownum in xrange(mysheet.nrows):
                    if rownum<startingRow:
                        continue
                    #get the row from sheet
                    row= mysheet.row_values(rownum)
                    #append the year column name or year data
                    if rownum==startingRow:
                        row.append("year_auto")
                    else:
                        row.append(str(year))
                    #if the format is unicode, encode it and convert to string
                    for i in xrange(len(row)):
                        if type(row[i]) is unicode:
                            row[i]= row[i].encode('utf8')
                        if row[i]=='':
                            row[i]="NULL"
                    #write the row to csv file
                    wr.writerow(row)
                print("Writing is done.")
                
            
        #In Elsevier dataset, empty values have been left blank like "". Awk finds this pattern and replaces them with \N, meaning NULL.
        def replaceEmptyNUll(filename, sheet):
            print("Replacing empty values with NULL.")
            os.system(replace_empty_command)
            print("Replacing done.")
           
            
            
ElsevierScopus()
             
             
             
            


