import mysql.connector

db_conn = mysql.connector.connect(host="tanlab6a.eastus.cloudapp.azure.com", user="user", password="hello123",database="events")
# db_conn = mysql.connector.connect(host="localhost", user="root", password="hello123", database="mydb")
db_cursor = db_conn.cursor()
db_cursor.execute('''
 CREATE TABLE cit
 (id INT NOT NULL AUTO_INCREMENT,
 class_id VARCHAR(250) NOT NULL,
 class_name VARCHAR(250) NOT NULL,
 instructor VARCHAR(250) NOT NULL,
 max_class_size INTEGER NOT NULL,
 date_created VARCHAR(100) NOT NULL,
 CONSTRAINT cit_pk PRIMARY KEY (id))
 ''')
db_cursor.execute('''
 CREATE TABLE student
 (id INT NOT NULL AUTO_INCREMENT,
 student_id VARCHAR(250) NOT NULL,
 student_name VARCHAR(250) NOT NULL,
 student_age INTEGER NOT NULL,
 start_date VARCHAR(250) NOT NULL,
 date_created VARCHAR(100) NOT NULL,
 CONSTRAINT student_pk PRIMARY KEY (id))
 ''')
db_conn.commit()
db_conn.close()
