# -*- coding: utf8 -*-

#Set pairs and self.year before use!!!
#assumes there is a folder with name Ccf_all in the current directory, create if not exists.
import pandas as pd
import Importer as imp
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


pairs=[('http://history.ccf.org.cn/sites/ccf/biaodan.jsp?contentId=2903028135780', 'Computer Architecture & Parallel and Distributed Computing & Storage System'),
       ('http://history.ccf.org.cn/sites/ccf/biaodan.jsp?contentId=2903028135856', 'Computer Networks'),
       ('http://history.ccf.org.cn/sites/ccf/biaodan.jsp?contentId=2903940690850', 'Network and Information Security'),
       ('http://history.ccf.org.cn/sites/ccf/biaodan.jsp?contentId=2903028135775', 'Software Engineering & System Software & Programming Language'),
       ('http://history.ccf.org.cn/sites/ccf/biaodan.jsp?contentId=2903940690081', 'Database & Data Mining & Knowledge Discovery'),
       ('http://history.ccf.org.cn/sites/ccf/biaodan.jsp?contentId=2903940690325', 'Theory of Computer Science'),
       ('http://history.ccf.org.cn/sites/ccf/biaodan.jsp?contentId=2903940690854', 'Computer Graphics and Multimedia'),
       ('http://history.ccf.org.cn/sites/ccf/biaodan.jsp?contentId=2903940690839', 'Artificial Intelligence'),
       ('http://history.ccf.org.cn/sites/ccf/biaodan.jsp?contentId=2903940690320', 'Computer-Human Interaction & Ubiquitous Computing'),
       ('http://history.ccf.org.cn/sites/ccf/biaodan.jsp?contentId=2903940690316', 'Interdisciplinary & Intergration & Inovation')]

class ccf:
    def __init__(self):
        self.year='2015'
        self.downloadCSV(pairs)
        self.import_query="LOAD DATA LOCAL INFILE 'Ccf_all/ccf.csv' INTO TABLE ccf FIELDS TERMINATED BY ',' ENCLOSED BY '\"' ESCAPED BY '\\\\' IGNORE 0 LINES"
        imp.Importer(self.import_query)
    #link finder
    #translator
    def read_website(self, url, category): #add new columns for rank, category and type
        file_name=str('./Ccf_all/ccf.csv')
        df = pd.read_html(url, header = 0)
        for i in range(2, 5): #journals
            df[i].rename(inplace = True, columns = {'序号': 'No.', '刊物简称': 'Acronym', '刊物全称': 'Journal', '出版社': 'Publisher', '网址': 'Website'})
            df[i]['Rank']=self.J_rank(i)
            df[i]['Category']=category
            df[i]['Type']='Journal'
            df[i]['Year']=self.year
            #file_name = str('./Ccf_all/Journal_Rank_'+ self.J_rank(i) + '__' + category + '.csv')
            df[i].to_csv(file_name, index = False, mode='a', header=False)
        for i in range(5, 8): #conferences
            df[i].rename(inplace = True, columns = {'序号': 'No.', '会议简称': 'Acronym', '会议全称': 'Conference', '出版社': 'Publisher', '网址': 'Website'})
            df[i]['Rank']=self.C_rank(i)
            df[i]['Category']=category
            df[i]['Type']='Conference'
            df[i]['Year']=self.year
            #file_name = str('./Ccf_all/Conference_Rank_' +self.C_rank(i) + '__' + category + '.csv')
            df[i].to_csv(file_name, index = False, mode='a', header=False)
    
    def J_rank(self, x):
        return {
            2 : 'A',
            3 : 'B',
            4 : 'C'
        }.get(x, 0)
    
    def C_rank(self, x):
        return {
            5 : 'A',
            6 : 'B',
            7 : 'C'
        }.get(x, 0)
        
    def downloadCSV(self, pairs):
        for pair in pairs:
            self.read_website(pair[0], pair[1])

c=ccf() 
