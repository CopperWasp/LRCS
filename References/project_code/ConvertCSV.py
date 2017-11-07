import xlrd
import csv
import datetime
import os

#method assumes starting row has the attribute names and the file is in the same folder as this script, 
def xlsToCsv(filename, sheet, startingRow, year=datetime.date.today().year-1):
    print "Xls to Csv is called for "+filename+", sheet "+str(sheet)+", year: "+str(year)
    with open(filename+'_sheet'+str(sheet)+'.csv', 'wb') as myCsvfile:
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
        
        
        
def xlsToCsvLastSheet(filename, startingRow, year=datetime.date.today().year-1):
    print "Xls to Csv is called for "+filename+", latest sheet, year: "+str(year)
    with open(filename+'_sheetLatest.csv', 'wb') as myCsvfile:
        wr=csv.writer(myCsvfile, delimiter="\t")
        myfile=xlrd.open_workbook(filename+'.xlsx', 'rU')
        mysheet=myfile.sheet_by_index(len(myfile.sheets)-2) #get the given sheet
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
        replaceEmptyNUll(filename, 'Latest')
                    
def replaceEmptyNUll(filename, sheet):
    print("Replacing empty values with NULL")
    command= """awk 'BEGIN { FS = OFS = "\t" } { for(i=1; i<=NF; i++) if($i ~ /^ *$/) $i = "\N" }; 1's """
    path= filename+"_sheet"+str(sheet)+".csv"
    final_command= command+path
    os.system(final_command)
    print("Replacing done.")

def replaceEmptyNUll_scimagojr(filename, sheet):
    command= """awk 'BEGIN { FS = OFS = "\t" } { for(i=1; i<=NF; i++) if($i == "-") $i = "\N" }; 1' """
    path= filename+"_sheet"+str(sheet)+".csv"
    final_command= command+path
    os.system(final_command)
    print("Replacing done.")

    

def convertAndProcess(filename, sheet, startingRow, year=datetime.date.today().year-1):
    xlsToCsv(filename, sheet, startingRow, year)
    replaceEmptyNUll(filename, sheet)

#Convert All Elsevier
#year=2016   
#for i in range (1,8):
#    convertAndProcess('elsevier0', i, 1, year)
#    year-=1
#    

#Convert All Scimagojr  
#n0='Scimagojr_all/'   
#n1='scimagojr'
#n2=2009
#for i in range(0,8):
#    name=n0+n1+str(n2)
#    xlsToCsv(name, 0, 0, n2)
#    replaceEmptyNUll_scimagojr(name, 0)
#    n2+=1
