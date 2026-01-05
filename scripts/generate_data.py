import random
import os

# This script simulates generating data for the Oracle Database
# and "generating" images (fetching placeholders) for the demo.

CATEGORIES = ["Men", "Women", "Boys", "Girls"]
COLORS = ["Red", "Blue", "Green", "Black", "White"]
ITEMS = ["Shoes", "T-Shirt", "Jeans", "Jacket"]

def generate_mock_data(num_items=20):
    data = []
    print("Generating mock inventory data...")
    for i in range(num_items):
        category = random.choice(CATEGORIES)
        color = random.choice(COLORS)
        item_type = random.choice(ITEMS)
        size = random.choice([6, 7, 8, 9, 10, "S", "M", "L"])
        price = round(random.uniform(20.0, 100.0), 2)
        name = f"{color} {item_type}"

        # In a real scenario, we would call Vertex AI Imagen here
        # image_url = generate_image_with_imagen(f"{color} {item_type} for {category}")

        # Using a placeholder service for the demo
        image_url = f"https://placehold.co/300x300?text={color}+{item_type}+{category}"

        row = {
            "id": i + 1,
            "name": name,
            "category": category,
            "size": size,
            "color": color,
            "price": price,
            "image_url": image_url
        }
        data.append(row)
        print(f"Generated: {row}")

    return data

def generate_sql_insert_statements(data):
    print("\nGeneraring SQL Insert Statements...")
    with open("scripts/init_db.sql", "w") as f:
        f.write("CREATE TABLE INVENTORY (ID NUMBER, NAME VARCHAR2(100), CATEGORY VARCHAR2(50), SIZE_VAL VARCHAR2(20), COLOR VARCHAR2(20), PRICE NUMBER, IMAGE_URL VARCHAR2(500));\n")
        for row in data:
            sql = f"INSERT INTO INVENTORY (ID, NAME, CATEGORY, SIZE_VAL, COLOR, PRICE, IMAGE_URL) VALUES ({row['id']}, '{row['name']}', '{row['category']}', '{row['size']}', '{row['color']}', {row['price']}, '{row['image_url']}');\n"
            f.write(sql)
    print("SQL script written to scripts/init_db.sql")

if __name__ == "__main__":
    mock_data = generate_mock_data()
    generate_sql_insert_statements(mock_data)
