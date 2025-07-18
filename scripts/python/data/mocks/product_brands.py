from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_product_brands(ref_data, inactive_ratio=0.01, delete_ratio=0.005):
    product_brands = []

    products = ref_data.get("products")
    brands = ref_data.get("brands")

    if not products or not brands:
        raise ValueError("Reference data for products and brands is missing")
    
    for product in products:
        brands_count = random.randint(1, 3)  
        chosen_brands = random.sample(brands, min(brands_count, len(brands)))
        for brand in chosen_brands:
            created_at, updated_at = generate_timestamps(3)
            product_brands.append({
                "product_id": product['product_id'],
                "brand_id": brand['brand_id'],
                "is_delete": random.random() < delete_ratio,
                "is_active": random.random() > inactive_ratio,
                "created_at": created_at,
                "updated_at": updated_at,
            })
    
    return product_brands

def insert_product_brands(product_brands):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO product_brands (
            product_id, brand_id, is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(product_id)s, %(brand_id)s, %(is_delete)s, 
            %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, product_brands)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(product_brands)} fake product brands inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    product_brands = generate_product_brands(ref_data)
    insert_product_brands(product_brands)