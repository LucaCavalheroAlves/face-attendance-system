import mysql.connector
# IMPORTANTE! pip install mysql-connector-python

def criar_conexão_com_MYSQL():
    mydb = mysql.connector.connect( 
    host="localhost", # Por favor, adapte para seu MYSQL
    user="root", # Por favor, adapte para seu MYSQL
    password="L160403!", # Por favor, adapte para seu MYSQL
    database="face_recognition" # Por favor, adapte para seu MYSQL
    )

    mycursor = mydb.cursor()
    return mydb, mycursor