from .connection import create_connection, close_connection
import sqlite3


def user_exists(email):
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM "USER" WHERE email = ?', (email,))
    user = cursor.fetchone()

    conn.close()
    return user is not None

def register_user(name, contact, email, user_type, password):
    if user_exists(email):
        return False

    try:
        conn = sqlite3.connect('plateful.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO USER (user_type, name, contact, email, password)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_type, name, contact, email, password))

        # Get the newly inserted user's ID
        user_id = cursor.lastrowid

        # Map user to corresponding table based on user_type
        if user_type == "FS Employee":
            cursor.execute('''
                    INSERT INTO FOOD_SUPPLIER (user_id, name, contact, email)
                    VALUES (?, ?, ?, ?)
                    ''', (user_id, name, contact, email))
        elif user_type == "NGO Employee":
            cursor.execute('''
                    INSERT INTO NGO (user_id, name, contact, email)
                    VALUES (?, ?, ?, ?)
                    ''', (user_id, name, contact, email))
        elif user_type == "BPLU":
            cursor.execute('''
                    INSERT INTO BPL_VERIFICATION (user_id, name, contact, email)
                    VALUES (?, ?, ?, ?)
                    ''', (user_id, name, contact, email))
        elif user_type == "StudentU":
            cursor.execute('''
                    INSERT INTO STUDENT_VERIFICATION (user_id, name, contact, email)
                    VALUES (?, ?, ?, ?)
                    ''', (user_id, name, contact, email))
        elif user_type == "Admin":
            cursor.execute('''
                    INSERT INTO ADMIN (admin_id, name, contact, email, password)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (user_id, name, contact, email, password))

        conn.commit()
        conn.close()
        print(f"User registered successfully and mapped to {user_type} table!")
        return True

    except Exception as e:
        print(f"Error registering user: {e}")
        conn.rollback()  # Rollback the transaction in case of an error
        conn.close()
        return False


def login_user(email, password):
    try:
        conn = sqlite3.connect('plateful.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM USER WHERE email = ? AND password = ?
        ''', (email, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None  # Return True if user exists, else False
    except Exception as e:
        print(f"Error logging in: {e}")
        return False


def add_food_item(name, restaurant_id, price, description, available):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO FOOD_ITEM (name, restaurant_id, price, description, available) VALUES (%s, %s, %s, %s, %s)"
            values = (name, restaurant_id, price, description, available)
            cursor.execute(query, values)
            connection.commit()
            print("Food item added successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)


def get_food_items():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM FOOD_ITEM"
            cursor.execute(query)
            food_items = cursor.fetchall()
            return food_items
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)


def delete_food_item(item_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM FOOD_ITEM WHERE item_id = %s"
            cursor.execute(query, (item_id,))
            connection.commit()
            print("Food item deleted successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)


def place_order(user_id, restaurant_id, order_time, status, total_amount):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO ORDER (user_id, restaurant_id, order_time, status, total_amount) VALUES (%s, %s, %s, %s, %s)"
            values = (user_id, restaurant_id, order_time, status, total_amount)
            cursor.execute(query, values)
            connection.commit()
            print("Order placed successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)


def get_orders():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM ORDER"
            cursor.execute(query)
            orders = cursor.fetchall()
            return orders
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)


def add_order_item(order_id, food_item_id, quantity, unit_price):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO ORDER_ITEM (order_id, food_item_id, quantity, unit_price) VALUES (%s, %s, %s, %s)"
            values = (order_id, food_item_id, quantity, unit_price)
            cursor.execute(query, values)
            connection.commit()
            print("Order item added successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)
