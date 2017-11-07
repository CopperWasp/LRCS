#Mysql connector to import files
import pymysql
import xlrd

class Importer:
    db_host= 'localhost'
    db_user= 'root'
    db_passwd= '123456'
    db_name= 'RANKING_DB'
    db_port=3306
    
    def __init__(self, query):
        self.connect()
        self.cursor.execute(query)
        self.database.commit()
        #self.printQueryResults() #not working yet
    
    def connect(self):
        print("Connecting to "+self.db_name)
        self.database= pymysql.connect (host= self.db_host,
                                   port=self.db_port,
                                   user= self.db_user,
                                   passwd=self.db_passwd,
                                   db=self.db_name,
                                   local_infile=True)
        self.cursor = self.database.cursor()
        
    def printQueryResults(self):
        print("Results for the last query:")
        for row in self.cursor:
            print(row)
            
    def disconnect(self):
        self.cursor.close()
        self.connection.close()
        print("Disconnected from db.")
           
    def loadXls(self, filename):
        print("Loading file: "+filename)
        self.xl=xlrd.open_workbook(filename)
        print(filename+" loaded.")

