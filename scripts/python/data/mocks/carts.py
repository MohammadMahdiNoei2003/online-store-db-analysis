from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps_list
import random

faker = Faker()
Faker.seed(42)
random.seed(42)

def generate_carts(ref_data, max_cart_per_user=6, inactive_ratio=0.1, delete_ratio=0.05):
    carts = []

    users = ref_data.get("users")

    if not users:
        raise ValueError("Reference data for users is missing")
    
    for user in users:
        user_id = user['user_id']
        num_carts = random.randint(0, max_cart_per_user)

        timestamps = generate_timestamps_list(num_carts)

        for i in range(num_carts):
            created_at, updated_at = timestamps[i]

            carts.append({
                "user_id": user['user_id'],
                "is_delete": random.random() < delete_ratio,
                "is_active": random.random() > inactive_ratio,
                "created_at": created_at,
                "updated_at": updated_at, 
            })

    return carts

def insert_carts(carts):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO carts (
            user_id, is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(user_id)s, %(is_delete)s, %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, carts)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(carts)} fake carts inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    carts = generate_carts(ref_data)
    insert_carts(carts)