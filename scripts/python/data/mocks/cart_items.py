from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps_list
import random

faker = Faker()
Faker.seed(42)
random.seed(42)

def generate_cart_items(ref_data, max_items_per_cart=10, inactive_ratio=0.1, delete_ratio=0.05):
    cart_items = []

    carts = ref_data.get("carts")
    products = ref_data.get("products")

    if not carts or not products:
        raise ValueError("Reference data for carts or products is missing")
    
    for cart in carts:
        cart_id = cart['cart_id']
        num_items = random.randint(1, max_items_per_cart)
        timestamps = generate_timestamps_list(num_items)

        product_sample = random.sample(products, min(num_items, len(products)))

        for i in range(num_items):
            product = product_sample[i % len(product_sample)]
            created_at, updated_at = timestamps[i]

            cart_items.append({
                "cart_id": cart_id,
                "product_id": product['product_id'],
                "quantity": random.randint(1, 5),
                "is_delete": random.random() < delete_ratio,
                "is_active": random.random() > inactive_ratio,
                "created_at": created_at,
                "updated_at": updated_at,
            })

    return cart_items

def insert_cart_items(cart_items):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO cart_items (
            cart_id, product_id, quantity, is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(cart_id)s, %(product_id)s, %(quantity)s, %(is_delete)s, %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, cart_items)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(cart_items)} fake cart items inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    cart_items = generate_cart_items(ref_data)
    insert_cart_items(cart_items)
