import mysql.connector

# db_conn = mysql.connector.connect(host="localhost", user="root",
# password="hello123", database="mydb")
db_conn = mysql.connector.connect(host="tanlab6a.eastus.cloudapp.azure.com", user="user", password="hello123",database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
 DROP TABLE cit, student
''')
db_conn.commit()
db_conn.close()