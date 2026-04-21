import sqlite3

## Connect to sqlite
connection=sqlite3.connect("student.db")

## Create a cursor object to inser records, create tables

cursor=connection.cursor()

## create the table
table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT)
"""

cursor.execute(table_info)

## Insert more records
cursor.execute("INSERT INTO STUDENT VALUES('Samarth','Data Science','A',90)")
cursor.execute("INSERT INTO STUDENT VALUES('Sagar','GenAi','A',89)")
cursor.execute("INSERT INTO STUDENT VALUES('Sanjay','DevOps','A',77)")
cursor.execute("INSERT INTO STUDENT VALUES('Gargi','Machine Learning','A',100)")
cursor.execute("INSERT INTO STUDENT VALUES('Gaurav','Big Data','A',69)")

## Display All Recored

print("The inserted record are")
data=cursor.execute("select * from STUDENT")

for row in data:
    print(row)

## Commit your changes
connection.commit()

## Close the connection
connection.close()