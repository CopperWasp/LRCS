#Needs to have a check functionality, if the data needs to be updated or not
#Everyone is feeding from same filepath ScimagojrAuto/scimagojr0_sheetLatest.csv make this a variable
#Put error catching clauses to some methods
from selenium import webdriver
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
#Attributes decided by MySQL are compatible with future imports, no need to do further modification.
#Empty values (in Scimagojr indicated by "-") need to be replaced by \N, to be type compatible with their respective fields, a bash script does this conversion.
#Scimagojr data set has a single sheet for each year, to update the database you only need to get the latest data.
#Scimagojr webpage has dropdown menus to select subject areas, subject categories, regions/countries, types and year. Selenium webdriver automatically chooses Computer Science as subject area and year as latest year for database update.
#After selecting the options from dropdown menus, Selenium clicks on the download button and starts downloading.
#If any connection problems occur and page loading can not catch up with scripts pace (normally script should implicitly wait), set wait variable below to increase wait time while page loads.
wait=0

#Other variables
import_query = "LOAD DATA LOCAL INFILE 'ScimagojrAuto/scimagojr0_sheetLatest2.csv' INTO TABLE Scimagojr FIELDS TERMINATED BY '\t' ENCLOSED BY '\"' ESCAPED BY '\\\\' IGNORE 1 LINES"
replace_empty_command= """awk 'BEGIN { FS = OFS = "\t" } { for(i=1; i<=NF; i++) if($i == "-") $i = "\N" }; 1's ScimagojrAuto/scimagojr0_sheetLatest.csv > ScimagojrAuto/scimagojr0_sheetLatest2.csv"""
starting_row=0 #For scimagojr, data starts from first row by attribute names.

class Scimagojr:

        def __init__(self):
            self.source_name='ScimagojrAuto/scimagojr' #File will be saved under ElsevierAuto folder
            self.file_extension= '.xlsx'
            self.DOMAIN= 'scimagojr.com'
            self.URL= 'http://www.scimagojr.com/journalrank.php'
            self.driver = webdriver.Chrome("./Chromedrivers/chromedriver_"+current_os)
            self.download_links=[]
            self.downloaded_file_path=self.source_name+str(0)
            self.converted_file_path=self.downloaded_file_path+"_sheetLatest.csv"
            self.update()
            
        def update(self): 
            print("Scimago Journal Rankings update is called.")
            self.scrape()
            self.Download()
            self.xlsToCsv(self.downloaded_file_path, 0, starting_row) #year must be current year -1, letting default value handle
            self.replaceEmptyNUll(self.converted_file_path)
            imp.Importer(import_query)
                  
        def fillSpecs(self): #choose computer science as subject area, assuming by default the latest is chosen
             #ele= Select(self.driver.find_element_by_xpath("//*[contains(text(), 'All subject')]"))
             field1= self.driver.find_element_by_xpath("//*[contains(text(), 'All subject areas')]")
             field1.click()
             field2=field1.find_element_by_xpath("//*[contains(text(), 'Computer Science')]")
             field2.click()

        def extractLinks(self):
            elems = self.driver.find_elements_by_xpath("//a[@href]")
            for elem in elems:
                if ("xlsx" in elem.get_attribute("href") or "xls" in elem.get_attribute("href")):
                    self.download_links.append(elem.get_attribute("href"))
            print("Extracted possible download links.")
        
        def scrape(self):
            self.driver.get_screenshot_as_png()
            self.driver.get(self.URL)
            self.fillSpecs()
            self.extractLinks()
            return self.download_links
        
        def printLinks(self):
            print("Extracted download links from Scimago Journal Rankings:")
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
        def xlsToCsv(self, filename, sheet, startingRow, year=datetime.date.today().year-1):
            print "XLS to CSV is called for "+filename+", sheet "+str(sheet)+", year: "+str(year)
            with open(self.converted_file_path, 'wb') as myCsvfile:
                wr=csv.writer(myCsvfile, delimiter="\t")
                myfile=xlrd.open_workbook(filename+'.xlsx', 'rU')
                mysheet=myfile.sheet_by_index(sheet) #get the given sheet
                print("Writing started")
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
                print("Writing is done")
            
        def replaceEmptyNUll(filename, sheet):
            print("Replacing empty values with NULL.")
            os.system(replace_empty_command)
            print("Replacing done.")
           
                  
Scimagojr()
             
             
             
            


