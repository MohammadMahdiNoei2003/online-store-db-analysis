from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps
from datetime import datetime
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_product_discounts(ref_data, delete_ratio=0.03):
    product_discounts = []

    products = ref_data.get("products")
    discounts = ref_data.get("discounts")

    if not products or not discounts:
        raise ValueError("Reference data for products and discounts in missing")
    
    for product in products:
        discount_count = random.randint(0, 6)
        chosen_discounts = random.sample(discounts, min(discount_count, len(discounts)))
        for discount in chosen_discounts:
            created_at, updated_at = generate_timestamps(3)
            expired_at = discount.get('expired_at')
            is_active = expired_at is None or expired_at > datetime.now()
            product_discounts.append({
                "product_id": product['product_id'],
                "discount_id": discount['discount_id'],
                "is_delete": random.random() < delete_ratio,
                "is_active": is_active,
                "created_at": created_at,
                "updated_at": updated_at,
            })
    
    return product_discounts

def insert_product_discounts(product_discounts):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO product_discounts (
            product_id, discount_id, is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(product_id)s, %(discount_id)s, %(is_delete)s, 
            %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, product_discounts)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(product_discounts)} fake product discounts inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    product_discount = generate_product_discounts(ref_data)
    insert_product_discounts(product_discount) 