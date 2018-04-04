import mysql.connector    
from tesla import Datareceive_tesla
import objectpath
import datetime

#the handler class for dealing with database operation

class DBoperator(object):
    def __init__(self):
        print("object created")
        file = open("creds.txt", "r") #mysql database credentials are stored in a txt file, without putting it to the github repo
        #TODO there should be a better way to do this
        parameters = file.read().splitlines() 
        self.user = parameters[0]
        self.password = parameters[1]
        self.host = parameters[2]
        self.database = parameters[3]
        file.close()         

    #pick the db table and push to each column 
    def push_to_database(self,table_name,database_values):
        
        cnx = mysql.connector.connect(user=self.user, password=self.password,
                        host=self.host,
                        database=self.database)

        database_values[0] = database_values[0] / 1000 #need to convert milisecond to seconds
        readable_timestamp = datetime.datetime.fromtimestamp(database_values[0]).strftime('%Y-%m-%d %H:%M:%S') #formatting timestamp do datetime
        
        print("database_values[0]")
        print(database_values[0])
        #creating MYQL statement string
        row_values = "(" + r'"' + readable_timestamp + r'"'
        for i in range(len(database_values)):
            if (i!=0):
                row_values += str(database_values[i])
            if i != len(database_values) - 1:
                row_values += ","        
        row_values += ");"
        print("printing row values")
        print(row_values)
        push_row_sql = """
            INSERT INTO """ + table_name + """
            VALUES """ + row_values
        
        print("push_row_sql")
        print(push_row_sql)

        try:
            cursor = cnx.cursor()
            cursor.execute(push_row_sql)
        finally:
            cnx.close()

