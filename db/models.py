from .connection import create_connection, close_connection

def register_user(name, contact, email, user_type, password):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''
            INSERT INTO USER (user_type, name, contact, email, password)
            VALUES (%s, %s, %s, %s, %s)
            ''', (user_type, name, contact, email, password))

            connection.commit()
            close_connection(connection)
            print("User registered successfully!")
            return True
        except Exception as e:
            print(f"Error registering user: {e}")
            return False


def login_user(email, password):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute('''
            SELECT * FROM USER WHERE email = %s AND password = %s
            ''', (email, password))
            user = cursor.fetchone()
            close_connection(connection)
            return user is not None
        except Exception as e:
            print(f"Error logging in: {e}")
            return False