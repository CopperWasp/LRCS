#similarity based table merger
import pymysql
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, Integer, String
from sqlalchemy.orm import mapper, create_session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def measureSimilarity(merged_dict):
    print "Measuring pairwise similarity of titles."
    all_titles=merged_dict.keys()
    vectorizer = TfidfVectorizer(stop_words='english', norm='l2', sublinear_tf=True)
    tfidf_matrix = vectorizer.fit_transform(all_titles)
    similarity_matrix= cosine_similarity(tfidf_matrix, tfidf_matrix)
    np.fill_diagonal(similarity_matrix, 0) #fill diagonal, max similarity will be on diagonal, same items
    a_1d = similarity_matrix.flatten() # Convert it into a 1D array
    idx_1d = a_1d.argsort()[-1000:] # find top 1000
    x_idx, y_idx = np.unravel_index(idx_1d, similarity_matrix.shape) # convert the idx_1d back into indices arrays for each dimension
    counter=0
    for x, y, in zip(x_idx, y_idx):
        if similarity_matrix[x][y]==1:
            counter+=1
            print(str(counter)+", Cosine Sim: "+str(similarity_matrix[x][y]))
            print "1: "+all_titles[x]
            print "2: "+all_titles[y]

class tableRow(object): #object for attributes in table row
    pass

class connector:
    db_host= 'localhost'
    db_user= 'root'
    db_passwd= '123456'
    db_name= 'RANKING_DB'
    db_port=3306

    def __init__(self):
        self.connect()

    def connect(self):
        print("Connecting to "+self.db_name+".")
        self.database= pymysql.connect (host= self.db_host,
                                   port=self.db_port,
                                   user= self.db_user,
                                   passwd=self.db_passwd,
                                   db=self.db_name,
                                   local_infile=True)
        self.cursor=self.database.cursor(pymysql.cursors.DictCursor)

    def getTable(self, table_name):
        self.cursor.execute("SELECT * FROM "+str(table_name))
        return self.cursor.fetchall()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()
        print("Disconnected from db.")

#get tables from the database
print "Fetching tables."
m= connector()
ccf= m.getTable("ccf")
elsevier= m.getTable("elsevier")
cwts= m.getTable("cwts")
scimago= m.getTable("scimagojr")
core= m.getTable("core")

#merge tables in the dictionary merged_dict
#merged_dict is in type <dict of dict> for fast lookup and matches
#if duplicate titles, merge their attributes
print "Merging tables."
merged_dict={}

for row in ccf:
    merged_dict[row["Title"]]= {"ccf_"+str(x): row[x] for x in row if x!="Title"}

for row in elsevier:
    if row["Title"] in merged_dict.keys():
        for key, value in row.items():
            merged_dict[row["Title"]]["elsevier_"+str(key)]=value
    else:
        merged_dict[row["Title"]]= {"elsevier_"+str(x): row[x] for x in row if x!="Title"}

for row in cwts:
    if row["Source title"] in merged_dict.keys():
        for key, value in row.items():
            merged_dict[row["Source title"]]["cwts_"+str(key)]=value
    else:
        merged_dict[row["Source title"]]= {"cwts_"+str(x): row[x] for x in row if x!="Source title"}

for row in scimago:
    if row["Title"] in merged_dict.keys():
        for key, value in row.items():
            merged_dict[row["Title"]]["scimago_"+str(key)]=value
    else:
        merged_dict[row["Title"]]= {"scimago_"+str(x): row[x] for x in row if x!="Title"}

for row in core:
    if row["Title"] in merged_dict.keys():
        for key, value in row.items():
            merged_dict[row["Title"]]["core_"+str(key)]=value
    else:
        merged_dict[row["Title"]]= {"core_"+str(x): row[x] for x in row if x!="Title"}

#transform merged_dict into type <dict_of_dict>
list_of_values=[]
for key, value in merged_dict.items():
    merged_dict[key]["Title"]= key
    list_of_values.append(merged_dict[key])

#get a list of unique attributes, and complete missing attributes with 'Null's
all_keys=set().union(*list_of_values)
for row in list_of_values:
    for key in all_keys:
        if key not in row.keys():
            row[key]='Null'

#create an empty table with list of all attributes, using SQLalchemy
print "Creating table MergedTable in database."
m.cursor.execute("DROP TABLE IF EXISTS MergedTable")
engine= create_engine("mysql+pymysql://root:123456@localhost/RANKING_DB")
metadata= MetaData(bind=engine)
t= Table('MergedTable', metadata, Column('id', Integer, primary_key=True), *(Column(col, String(500)) for col in all_keys))
metadata.create_all()

#create row objects from data in list_of_values and insert into database table
print "Inserting data into table."
mapper(tableRow, t)
row_objects=[]
session= create_session(bind=engine, autocommit=False, autoflush=True)
for row in list_of_values:
    row_obj= tableRow()
    for key, value in row.items():
        setattr(row_obj, key , value)
    session.add(row_obj)
    session.commit()

#create a fulltext index on table
print "Creating FULLTEXT index by Title attribute on table for similarity based seach."
m.cursor.execute("ALTER TABLE MergedTable ADD FULLTEXT INDEX title_index (Title)")

#try if works
m.cursor.execute("SELECT * FROM MergedTable WHERE MATCH(Title) AGAINST('Artificial Intelligence Conference' IN NATURAL LANGUAGE MODE)")
#print m.cursor.fetchall()
print "Done."

#check similar titles
measureSimilarity(merged_dict)
