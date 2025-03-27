# import sqlite3
#
# def setup_database():
#     conn = sqlite3.connect("plateful.db")
#     cursor = conn.cursor()
#
#     # Fetch existing suppliers
#     cursor.execute("SELECT restaurant_id FROM FOOD_SUPPLIER")
#     suppliers = cursor.fetchall()  # List of (restaurant_id,)
#     print("Existing Suppliers:", suppliers)
#
#     # Check if food items already exist
#     cursor.execute("SELECT COUNT(*) FROM FOOD_ITEM")
#
#     food_items = [
#         (1, "Masala Dosa", 120.0, "Crispy dosa with spiced potato filling", 1),
#         (1, "Idli Sambar", 80.0, "Soft idlis served with sambar and chutney", 1),
#         (2, "Paneer Butter Masala", 200.0, "Rich and creamy paneer curry", 1),
#         (2, "Tandoori Roti", 40.0, "Clay oven-baked roti", 1),
#         (3, "Biryani", 250.0, "Fragrant basmati rice with spices", 1),
#         (3, "Butter Chicken", 280.0, "Creamy tomato-based chicken curry", 1),
#         (4, "Pasta Alfredo", 180.0, "Creamy Italian pasta with cheese", 1),
#         (4, "Garlic Bread", 90.0, "Toasted bread with garlic butter", 1),
#         (5, "Chocolate Brownie", 150.0, "Rich and fudgy chocolate brownie", 1),
#         (5, "Fruit Salad", 130.0, "Fresh seasonal fruits with honey drizzle", 1),
#         (5, "Cold Coffee", 110.0, "Chilled coffee with ice cream", 1),
#         (5, "Mojito", 90.0, "Refreshing mint and lemon drink", 1),
#     ]
#
#     # Insert food items only for existing suppliers
#     for item in food_items:
#         restaurant_id = item[0]
#         if any(supplier[0] == restaurant_id for supplier in suppliers):
#             cursor.execute("""
#                 INSERT INTO FOOD_ITEM (restaurant_id, name, price, description, available)
#                 VALUES (?, ?, ?, ?, ?)
#             """, item)
#
#     conn.commit()
#     conn.close()
#     print("✅ Database setup complete! Existing suppliers retained, and new dishes added.")
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
email = "00005"
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

