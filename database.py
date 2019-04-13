import mysql.connector

config ={
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'geekworld',
    'buffered':True
}


def connections():
    conn= mysql.connector.connect(**config)
    c = conn.cursor()
    return c, conn
