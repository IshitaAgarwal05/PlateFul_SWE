from .connection import create_connection, close_connection
import sqlite3


def user_exists(email):
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM "USER" WHERE email = ?', (email,))
    user = cursor.fetchone()

    conn.close()
    return user is not None


def is_student_in_list(student_id, institution):
    """Check if student exists in STUDENT_LIST table"""
    try:
        conn = sqlite3.connect("plateful.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM STUDENT_LIST 
            WHERE student_id = ? AND institution = ?
        ''', (student_id, institution))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error checking student list: {e}")
        return False


def is_bpl_in_list(bpl_card_number, name, location):
    """Check if BPL user exists in BPL_LIST table"""
    try:
        conn = sqlite3.connect("plateful.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM BPL_LIST 
            WHERE bpl_card_number = ? AND name = ? AND location = ?
        ''', (bpl_card_number, name, location))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error checking BPL list: {e}")
        return False


def register_user(name, contact, email, location, user_type, password, student_id=None, institution=None,
                  bpl_card_number=None):
    if user_exists(email):
        return False, "User already exists with this email"

    try:
        conn = sqlite3.connect('plateful.db')
        cursor = conn.cursor()

        # Additional verification for StudentU and BPLU
        if user_type == "StudentU":
            if not student_id or not institution:
                return False, "Student ID and Institution are required"
            if not is_student_in_list(student_id, institution):
                return False, "Student not found in official records. Please check your details."

        elif user_type == "BPLU":
            if not bpl_card_number:
                return False, "BPL card number is required"
            if not is_bpl_in_list(bpl_card_number, name, location):
                return False, "BPL card holder not found in official records. Please check your details."

        # Insert into USER table
        cursor.execute('''
        INSERT INTO USER (user_type, name, contact, email, location, password)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_type, name, contact, email, location, password))

        user_id = cursor.lastrowid

        # Map user to corresponding table
        if user_type == "FS Employee":
            cursor.execute('''
                INSERT INTO FOOD_SUPPLIER (restaurant_id, name, contact, email, location)
                VALUES (?, ?, ?, ?, ?)
                ''', (user_id, name, contact, email, location))
        elif user_type == "NGO Employee":
            cursor.execute('''
                INSERT INTO NGO (ngo_id, name, contact, email, location)
                VALUES (?, ?, ?, ?, ?)
                ''', (user_id, name, contact, email, location))
        elif user_type == "BPLU":
            cursor.execute('''
                INSERT INTO BPL_VERIFICATION (user_id, bpl_card_number, name, contact, email, location)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, bpl_card_number, name, contact, email, location))
        elif user_type == "StudentU":
            cursor.execute('''
                INSERT INTO STUDENT_VERIFICATION (user_id, student_id, institution, name, contact, email, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, student_id, institution, name, contact, email, location))
        elif user_type == "Admin":
            cursor.execute('''
                INSERT INTO ADMIN (name, contact, email, location, password)
                VALUES (?, ?, ?, ?, ?)
                ''', (name, contact, email, location, password))

        conn.commit()
        conn.close()
        return True, "Registration successful"

    except Exception as e:
        print(f"Error registering user: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False, f"Registration failed: {str(e)}"


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


def get_user_type(email):
    """Returns the user type (NGO, BPLU, etc.) for the given email"""
    try:
        conn = sqlite3.connect("plateful.db")
        cursor = conn.cursor()

        cursor.execute('SELECT user_type FROM "USER" WHERE email = ?', (email,))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else "unknown"
    except Exception as e:
        print(f"Error getting user type: {e}")
        return "unknown"

    except Exception as e:
        print(f"Error getting user type: {e}")
        return None


def get_food_suppliers(user_id=1):
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()

    # Pehle user ki location fetch karni hai
    cursor.execute('SELECT location FROM "USER" WHERE user_id = ?', (user_id,))
    user_location = cursor.fetchone()

    if not user_location:
        return []  # Agar user ka location nahi mila toh khali list return karenge

    user_location = user_location[0]  # Tuple se value nikal lo

    # Ab matching food suppliers nikalenge
    cursor.execute("SELECT name, image, rating, time FROM food_supplier WHERE location = ?", (user_location,))
    suppliers = cursor.fetchall()

    conn.close()

    return [{"name": name, "image": image, "rating": rating, "time": time} for name, image, rating, time in suppliers]



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


def update_food_item_quantity(item_id: int, quantity_purchased: int):
    """Update the quantity of a food item after purchase"""
    conn = sqlite3.connect('plateful.db')
    cursor = conn.cursor()
    try:
        # Get current quantity
        cursor.execute("SELECT quantity FROM FOOD_ITEM WHERE item_id = ?", (item_id,))
        current_quantity = cursor.fetchone()[0]

        new_quantity = current_quantity - quantity_purchased
        if new_quantity <= 0:
            # Update quantity and set available to 0 if none left
            cursor.execute(
                "UPDATE FOOD_ITEM SET quantity = 0, available = 0 WHERE item_id = ?",
                (item_id,)
            )
        else:
            # Just update the quantity
            cursor.execute(
                "UPDATE FOOD_ITEM SET quantity = ? WHERE item_id = ?",
                (new_quantity, item_id)
            )

        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating quantity: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()