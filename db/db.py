# import mysql.connector
#
# db = mysql.connector.connect(
#     host="localhost",
#     user="your_mysql_username",        # Replace with your MySQL username
#     password="your_mysql_password",    # Replace with your MySQL password
#     database="your_database_name"      # Replace with your database name
# )

import sqlite3

def insert_user(user_type, name, contact, email):
    conn = sqlite3.connect('plateful.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO USER (user_type, name, contact, email)
    VALUES (?, ?, ?, ?)
    ''', (user_type, name, contact, email))
    conn.commit()
    conn.close()

def fetch_users():
    conn = sqlite3.connect('plateful.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM USER')
    users = cursor.fetchall()
    conn.close()
    return users