from faker import Faker
import random
from db.connection import get_connection
from utils import generate_timestamps

fake = Faker()
Faker.seed(42)
random.seed(42)

CATEGORY_NAMES = [
    "Electronics",
    "Home & Kitchen",
    "Fashion",
    "Health & Personal Care",
    "Sports & Outdoors",
    "Books",
    "Toys & Games",
    "Office Supplies",
    "Automotive",
    "Beauty & Cosmetics",
    "Pet Supplies",
    "Groceries",
    "Baby Products",
    "Tools & Hardware",
    "Garden & Outdoor",
    "Jewelry",
    "Musical Instruments",
    "Footwear",
    "Mobile Accessories",
    "Computer & Accessories",
]

def generate_categories(names, inactive_ratio=0.05, delete_ratio=0.02):
    categories = []

    for name in names:
        created_at, updated_at = generate_timestamps(3)

        categories.append({
            "name": name,
            "is_active": random.random() > inactive_ratio,
            "is_delete": random.random() < delete_ratio,
            "created_at": created_at,
            "updated_at": updated_at
        })

    return categories

def insert_categories(categories):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO categories (
            name, is_active, is_delete, created_at, updated_at
        )
        VALUES (%(name)s, %(is_active)s, %(is_delete)s, %(created_at)s, %(updated_at)s);
    """

    cursor.executemany(query, categories)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(categories)} categories inserted.")

if __name__ == "__main__":
    categories = generate_categories(CATEGORY_NAMES)
    insert_categories(categories)
