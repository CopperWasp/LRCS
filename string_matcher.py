#read the data into dict from one source

#read the other source while comparing similarity 
    #1- check if we have the same
        #if yes do nothing, join the records
        #if no:
                #check the similarity (word by word similarity should be good)
                #if high -> match and join
                #if low -> create another record
                
import Levenshtein
import csv
import fuzzy_matcher as fuzz

filepaths=["Elsevier_all/elsevier0_sheet1.csv", "CoreAuto/Core0_sheetLatest2.csv", "Scimagojr_all/scimagojr2016_sheet0.csv"]
                              
dict={}

def check_and_add(dictionary, data): #d is dict
    if (data in dictionary):
        dictionary[data]+=1
        
    elif check_similarity(dictionary, data):
       print "Similar pair found: "+data 
        
    else:
        dict[data]=1
        
def check_similarity(dictionary, data):
    for record in dictionary:
        if Levenshtein.ratio(record, data)>0.7:
            return fuzz.is_ci_token_stopword_match(record, data)
                
for filename in filepaths:
    with open (filename, 'r') as csvinput:
        reader=csv.reader(csvinput, delimiter="\t")
        for row in reader:
            if len(row)>1:
                check_and_add(dict, row[1])
                    
        
        
        
        
                
        
    