from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps_list
import random

faker = Faker()
Faker.seed(42)
random.seed(42)

def generate_wishlists(ref_data, max_items_per_wishlist=10, inactive_ratio=0.01, delete_ratio=0.2):
    wishlists = []

    users = ref_data.get("users")
    products = ref_data.get("products")

    if not users or not products:
        raise ValueError("Reference data for users or products is missing")
    
    for user in users:
        user_id = user['user_id']
        num_products = random.randint(1, max_items_per_wishlist)
        timestamps = generate_timestamps_list(num_products)

        product_sample = random.sample(products, min(num_products, len(products)))

        for i, product in enumerate(product_sample):
            product = product_sample[i % len(product_sample)]

            created_at, updated_at = timestamps[i]

            wishlists.append({
                "user_id": user_id,
                "product_id": product['product_id'] if random.random() > 0.4 else None,
                "is_delete": random.random() < delete_ratio,
                "is_active": random.random() > inactive_ratio,
                "created_at": created_at,
                "updated_at": updated_at,
            })

    return wishlists

def insert_wishlists(wishlists):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO wishlists (
            user_id, product_id, is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(user_id)s, %(product_id)s, %(is_delete)s, 
            %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, wishlists)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(wishlists)} fake wishlists inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    wishlists = generate_wishlists(ref_data)
    insert_wishlists(wishlists)