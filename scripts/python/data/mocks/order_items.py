from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps_list
import random

faker = Faker()
Faker.seed(42)
random.seed(42)

def generate_order_items(ref_data, max_items_per_order=10, inactive_ratio=0.15, delete_ratio=0.1):
    order_items = []

    orders = ref_data.get("orders")
    products = ref_data.get("products")

    if not orders or not products:
        raise ValueError("Reference data for orders or products is missing")
    
    for order in orders:
        order_id = order['order_id']
        num_items = random.randint(1, max_items_per_order)
        timestamps = generate_timestamps_list(num_items)

        products_sample = random.sample(products, min(num_items, len(products)))

        for i in range(num_items):
            product = products_sample[i % len(products_sample)]
            created_at, updated_at = timestamps[i]

            order_items.append({
                "order_id": order_id,
                "product_id": product['product_id'],
                "total_quantity": random.randint(1, 15),
                "is_delete": random.random() < delete_ratio,
                "is_active": random.random() > inactive_ratio,
                "created_at": created_at,
                "updated_at": updated_at, 
            })
    
    return order_items

def insert_order_items(order_items):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO order_items (
            order_id, product_id, total_quantity, 
            is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(order_id)s, %(product_id)s, %(total_quantity)s, 
            %(is_delete)s, %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, order_items)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(order_items)} fake order items inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    order_items = generate_order_items(ref_data)
    insert_order_items(order_items)