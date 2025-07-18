from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps
from datetime import datetime
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_category_discounts(ref_data, delete_ratio=0.03):
    category_discounts = []

    categories = ref_data.get("categories")
    discounts = ref_data.get("discounts")

    if not categories or not discounts:
        raise ValueError("Reference data for categories and discounts in missing")
    
    for category in categories:
        discount_count = random.randint(0, 3)
        chosen_discounts = random.sample(discounts, min(discount_count, len(discounts)))
        for discount in chosen_discounts:
            created_at, updated_at = generate_timestamps(3)
            expired_at = discount.get('expired_at')
            is_active = expired_at is None or expired_at > datetime.now()
            category_discounts.append({
                "category_id": category['category_id'],
                "discount_id": discount['discount_id'],
                "is_delete": random.random() < delete_ratio,
                "is_active": is_active,
                "created_at": created_at,
                "updated_at": updated_at,
            })
    
    return category_discounts

def insert_category_discounts(category_discounts):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO category_discounts (
            category_id, discount_id, is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(category_id)s, %(discount_id)s, %(is_delete)s, 
            %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, category_discounts)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(category_discounts)} fake category discounts inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    category_discount = generate_category_discounts(ref_data)
    insert_category_discounts(category_discount) 