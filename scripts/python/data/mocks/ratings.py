from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps_list
import random

faker = Faker()
Faker.seed(42)
random.seed(42)

def generate_ratings(ref_data, max_ratings_per_user=5, verified_ratio=0.6, inactive_ratio=0.02, delete_ratio=0.1):
    ratings = []

    users = ref_data.get("users")
    products = ref_data.get("products")

    if not users or not products:
        raise ValueError("Reference data for users or products is missing")

    for user in users:
        user_id = user['user_id']
        num_ratings = random.randint(1, max_ratings_per_user)
        timestamps = generate_timestamps_list(num_ratings)

        product_sample = random.sample(products, min(num_ratings, len(products)))

        for i, product in enumerate(product_sample):
            created_at, updated_at = timestamps[i]

            ratings.append({
                "user_id": user_id,
                "product_id": product['product_id'],
                "rate": random.randint(1, 5),
                "is_verified_purchase": random.random() < verified_ratio,
                "is_delete": random.random() < delete_ratio,
                "is_active": random.random() > inactive_ratio,
                "created_at": created_at,
                "updated_at": updated_at,
            })

    return ratings

def insert_ratings(ratings):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO ratings (
            user_id, product_id, rate, is_verified_purchase, 
            is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(user_id)s, %(product_id)s, %(rate)s, %(is_verified_purchase)s,
            %(is_delete)s, %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, ratings)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(ratings)} fake ratings inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    ratings = generate_ratings(ref_data)
    insert_ratings(ratings)
