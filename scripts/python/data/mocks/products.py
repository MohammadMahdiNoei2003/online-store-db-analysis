from faker import Faker
import random 
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps

faker = Faker()
Faker.seed(42)
random.seed(42)

def generate_products(n, ref_data, inactive_ratio=0.1, delete_ratio=0.05):
    products = []

    categories = ref_data.get("categories")

    if not categories:
        raise ValueError("Reference data for categories is missing")
    
    sku_set = set()

    for _ in range(n):
        created_at, updated_at = generate_timestamps(3)

        sku = None
        while True:
            sku_candidate = faker.unique.bothify(text='??-#####').upper()
            if sku_candidate not in sku_set:
                sku = sku_candidate
                sku_set.add(sku)   
                break

        products.append({
            "category_id": random.choice(categories)['category_id'],
            "name": faker.catch_phrase(),
            "sku": sku,
            "description": faker.text(max_nb_chars=100),
            "quantity": random.randint(0, 1000),
            "is_active": random.random() > inactive_ratio,
            "is_delete": random.random() < delete_ratio,
            "created_at": created_at,
            "updated_at": updated_at,
        })
    return products

def insert_products(products):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO products (
            category_id, name, sku, description, quantity, is_active, is_delete,
            created_at, updated_at
        )
        VALUES (
            %(category_id)s, %(name)s, %(sku)s, %(description)s, %(quantity)s,
            %(is_active)s, %(is_delete)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, products)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(products)} fake products inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    products = generate_products(4000, ref_data)
    insert_products(products)
