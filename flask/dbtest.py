import mysql.connector


conn = mysql.connector.connect(host = 'localhost' ,user="root", password ='',database='face',port = 3306)
cursor = conn.cursor()



cursor.execute("show tables")
#data = cursor.fetchall()
#print(data)
for x in cursor:
    print(x)


conn.close()