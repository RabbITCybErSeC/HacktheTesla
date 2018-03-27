import mysql.connector    
from tesla import Datareceive_tesla
import objectpath

class DBoperator(object):
    def __init__(self):
        print("object created")
        file = open("../creds.txt", "r") 
        parameters = file.read().splitlines() 
        self.user = parameters[0]
        self.password = parameters[1]
        self.host = parameters[2]
        self.database = parameters[3]
        file.close()         

    def push_to_database(self,table_name,database_values):
        
        cnx = mysql.connector.connect(user=self.user, password=self.password,
                        host=self.host,
                        database=self.database)
        row_values = "("
        for i in range(len(database_values)):
            row_values += str(database_values[i])
            if i != len(database_values) - 1:
                row_values += ","        
        row_values += ");"
        print(row_values)
        push_row_sql = """
            INSERT INTO location_logs
            VALUES """ + row_values

        try:
            cursor = cnx.cursor()
            cursor.execute(push_row_sql)
        finally:
            cnx.close()


    def push_longtitude_latitude(self,json_data):

        tree_obj = objectpath.Tree(json_data)
        battery_range = tuple(tree_obj.execute('$..battery_range'))
        time_stamp = tuple(tree_obj.execute('$..timestamp'))

        
        cnx = mysql.connector.connect(user=self.user, password=self.password,
                        host=self.host,
                        database=self.database)

        row_values = "(" + str(time_stamp[0]) + "," + str(battery_range[0]) + "," + str(battery_range[0]) + ");"


        push_row_sql = """
            INSERT INTO location_logs
            VALUES """ + row_values

        try:
            cursor = cnx.cursor()
            cursor.execute(push_row_sql)
        finally:
            cnx.close()
        #result = cursor.fetchall()
        #print(result)
        #finally:
        #    cnx.close()           
        
#        INSERT INTO table_name
#VALUES (value1, value2, value3, ...); 

#        cursor = cnx.cursor()
#        cursor.execute()


        


#try:
#   cursor = cnx.cursor()
#   cursor.execute("""
#      CREATE TABLE location_logs (
#          timestamp varchar(255),
#          longtitude float,
#          latitude float
#      ) 
#   """)
   #result = cursor.fetchall()
   #print(result)
#finally:
#    cnx.close()