# import sqlite3
#
#
# def setup_database():
#     conn = sqlite3.connect("plateful.db")
#     cursor = conn.cursor()
#
#     # Create FOOD_SUPPLIER table (without menu column)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS FOOD_SUPPLIER (
#             restaurant_id INTEGER PRIMARY KEY,
#             name TEXT NOT NULL,
#             location TEXT NOT NULL,
#             contact TEXT NOT NULL,
#             is_active BOOLEAN DEFAULT 1,
#             rating INTEGER,
#             email TEXT UNIQUE,
#             description TEXT
#         );
#     """)
#
#     # Create FOOD_ITEM table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS FOOD_ITEM (
#             item_id INTEGER PRIMARY KEY,
#             restaurant_id INTEGER,
#             name TEXT NOT NULL,
#             price REAL NOT NULL,
#             description TEXT,
#             available BOOLEAN DEFAULT 1,
#             FOREIGN KEY (restaurant_id) REFERENCES FOOD_SUPPLIER(restaurant_id) ON DELETE CASCADE
#         );
#     """)
#
#     # Insert sample data if not already present
#     cursor.execute("SELECT COUNT(*) FROM FOOD_SUPPLIER")
#     if cursor.fetchone()[0] == 0:
#         cursor.execute(
#             "INSERT INTO FOOD_SUPPLIER (name, location, contact, rating, email, description) VALUES ('Spicy Delight', 'New York', '1234567890', 5, 'spicy@food.com', 'Authentic spicy dishes')")
#         cursor.execute(
#             "INSERT INTO FOOD_SUPPLIER (name, location, contact, rating, email, description) VALUES ('Sweet Treats', 'Los Angeles', '0987654321', 4, 'sweet@food.com', 'Delicious desserts')")
#
#     cursor.execute("SELECT COUNT(*) FROM FOOD_ITEM")
#     if cursor.fetchone()[0] == 0:
#         cursor.execute(
#             "INSERT INTO FOOD_ITEM (restaurant_id, name, price, description, available) VALUES (1, 'Spicy Burger', 9.99, 'A fiery burger with jalapenos', 1)")
#         cursor.execute(
#             "INSERT INTO FOOD_ITEM (restaurant_id, name, price, description, available) VALUES (1, 'Hot Wings', 12.99, 'Crispy chicken wings with hot sauce', 1)")
#         cursor.execute(
#             "INSERT INTO FOOD_ITEM (restaurant_id, name, price, description, available) VALUES (2, 'Chocolate Cake', 5.99, 'Rich chocolate cake with frosting', 1)")
#
#     conn.commit()
#     conn.close()
#     print("✅ Database setup complete!")
#
#
# setup_database()





import sqlite3


def get_supplier_menu(email):
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()

    query = """
    SELECT fs.restaurant_id, fs.name, fs.location, fs.contact, fs.rating,
           fi.item_id, fi.name AS item_name, fi.price, fi.description, fi.available
    FROM FOOD_SUPPLIER fs
    JOIN FOOD_ITEM fi ON fs.restaurant_id = fi.restaurant_id
    WHERE fs.email = ?;
    """

    cursor.execute(query, (email,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return None  # No data found

    # Structure the data into a dictionary
    supplier_info = {
        "restaurant_id": rows[0][0],
        "name": rows[0][1],
        "location": rows[0][2],
        "contact": rows[0][3],
        "rating": rows[0][4],
        "menu": []
    }

    for row in rows:
        supplier_info["menu"].append({
            "item_id": row[5],
            "name": row[6],
            "price": row[7],
            "description": row[8],
            "available": row[9]
        })

    return supplier_info


# Test the function
email = "00001"
supplier_menu = get_supplier_menu(email)

if supplier_menu:
    print(f"🍽️ Restaurant: {supplier_menu['name']} ({supplier_menu['location']})")
    print(f"📞 Contact: {supplier_menu['contact']}")
    print(f"⭐ Rating: {supplier_menu['rating']}/5")
    print("\n📜 Menu:")
    for item in supplier_menu["menu"]:
        status = "✅ Available" if item["available"] else "❌ Not Available"
        print(f"- {item['name']} (₹{item['price']}) - {item['description']} [{status}]")
else:
    print("❌ No supplier found for this email.")

