#Needs to have a check functionality, if the data needs to be updated or not
#Put error catching clauses to some methods
#COMMANDS NEED TO BE REVIEWED!
#replace empty null duzeltilecek, replace etmeden oluyor ama database degisirse olur mu acaba
#for all data sources change current year to the existing year+1
#Core icin tum data sourcelari importla
#Core a ERA ekle
from selenium import webdriver
import urllib
import time
import datetime
import csv
import os
import Importer as imp




#!!!!Set the operating system before running this script following the example below!!!!
current_os="mac"
#current_os="linux"
#current_os="windows.exe"

#NOTES TO READER/USER
#CORE's latest data in 2017 is CORE2017
#Attribute names does not come with data source, they have been acquired from webpage, see the note in the Core_all folder for further info.
#Empty values (in Core indicated by "") need to be replaced by \N, to be type compatible with their respective fields, a bash script does this conversion.
#Core dataset has a single sheet for each year, it is enough to download and import the latest released data.
#Export button provided to download file is a submit button and download link is not directly accessible.
#Core webpage has dropdown menus to select year. When you open the page the latest source is already chosen and all core needs to do is click on search and export.
#After selecting the options from dropdown menus, Selenium clicks on the Export button and starts downloading.
#Core directly provides comma separated CSV format.
#If any connection problems occur and page loading can not catch up with scripts pace (normally script should implicitly wait), set wait variable below to increase wait time while page loads.
wait=0 

#Other variables
number_of_cols=9
year=2016
default_download_path="/users/ege/Downloads"
remove_command="rm "+default_download_path+"/CORE*.csv"
move_file_command="mv "+default_download_path+"/CORE.CSV ./CoreAuto/Core0_sheetLatest.csv"
import_query = "LOAD DATA LOCAL INFILE 'CoreAuto/Core0_sheetLatest2.csv' INTO TABLE Core FIELDS TERMINATED BY ',' ENCLOSED BY '\"' ESCAPED BY '\\\\'" #dont ignore any lines
#replace_empty_command= """awk 'BEGIN { FS = OFS = "," } { for(i=1; i<=NF; i++) if($i == "-") $i = "\N" }; 1's CoreAuto/Core0_sheetLatest.csv > CoreAuto/Core0_sheetLatest_med.csv"""
replace_empty_command="""awk 'BEGIN { FS = OFS = "," } { for(i=1; i<=NF; i++) if($i ~ /^ *$/) $i = "\N" }; 1's CoreAuto/Core0_sheetLatest.csv > CoreAuto/Core0_sheetLatest_med.csv"""
starting_row=0 #For core, data starts from first row by attribute names.

class Core:

        def __init__(self):
            self.filename="CORE.csv"
            self.source_name='CoreAuto/core' #File will be saved under CoreAuto folder
            self.file_extension= '.csv'
            self.DOMAIN= 'core.edu.au'
            self.URL= 'http://portal.core.edu.au/conf-ranks/'
            self.driver = webdriver.Chrome("./Chromedrivers/chromedriver_"+current_os)
            self.download_links=[]
            self.downloaded_file_path=self.source_name+str(0)
            self.converted_file_path=self.downloaded_file_path+"_sheetLatest.csv"
            self.update()
            
        def update(self): 
            print("Core Conference Rankings update is called.")
            os.system(remove_command)
            self.scrape()
            self.moveFile()
            #year must be current year -1, letting default value handle
            #self.replaceEmptyNUll(self.converted_file_path)
            #Add columns to standardize
            #self.addYearColumn() 
            self.replace_and_add_columns()
            imp.Importer(import_query)
                  
        def fillSpecs_and_download(self): #choose computer science as subject area, assuming by default the latest is chosen
             #ele= Select(self.driver.find_element_by_xpath("//*[contains(text(), 'All subject')]"))
             self.driver.find_element_by_xpath("//input[@type='submit']").click()
             self.driver.find_element_by_xpath("//input[@type='submit' and @value='Export']").click()
            
        def moveFile(self):
            print("Moving the file to its corresponding directory.")
            os.system(move_file_command)
            print("Moving done.")
               
        def scrape(self):
            os.system(remove_command)#remove same named files in Downloads
            self.driver.get_screenshot_as_png()
            self.driver.get(self.URL)
            self.fillSpecs_and_download()
            
            while not os.path.exists(default_download_path+"/"+self.filename):
                time.sleep(1)

            if os.path.isfile(default_download_path+"/"+self.filename):
                return
            else:
                raise ValueError("This isn't a file!")

        def waiter(self, amount):
            time.sleep(amount)
            
        def replaceEmptyNull(self):
            print("Replacing empty values with NULL.")
            os.system(replace_empty_command)
            print("Replacing done.")
           
        def replace_and_add_columns(self):
            #self.replaceEmptyNull()
            filename="CoreAuto/Core0_sheetLatest_med.csv"
            output="CoreAuto/Core0_sheetLatest2.csv"
            with open(filename,'r') as csvinput:
                with open(output, 'w') as csvoutput:
                    writer = csv.writer(csvoutput, lineterminator='\n')
                    reader = csv.reader(csvinput)

                    for row in reader:
                        while(len(row)<number_of_cols):
                            row.append("\N")
                        row.append(year)
                        writer.writerow(row)
      
            
        
           
                  
Core()
             
             
             
            


