import mysql.connector
from mysql.connector import Error
import sqlite3

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='PlateFulDB',  # Replace with your actual database name
            user='ishita',          # Replace with your actual username
            password='heha'         # Replace with your actual password
        )
        if connection.is_connected():
            print("Connection to database successful!")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed.")


def initialize_database():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Create the database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS PlateFulDB")
            print("Database created or already exists.")

            # Switch to the PlateFulDB database
            cursor.execute("USE PlateFulDB")

            # Create tables
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS USER (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                user_type VARCHAR(50),
                name VARCHAR(255),
                contact VARCHAR(50),
                email VARCHAR(255),
                password VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
            connection.commit()
            print("Tables initialized successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)