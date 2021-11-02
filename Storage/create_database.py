import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE cit
          (id INTEGER PRIMARY KEY ASC, 
           class_id VARCHAR(250) NOT NULL,
           class_name VARCHAR(250) NOT NULL,
           instructor VARCHAR(250) NOT NULL,
           max_class_size INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE student
          (id INTEGER PRIMARY KEY ASC, 
           student_id VARCHAR(250) NOT NULL,
           student_name VARCHAR(250) NOT NULL,
           student_age INTEGER NOT NULL,
           start_date INTEGER NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
