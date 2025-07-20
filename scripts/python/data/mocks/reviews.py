from faker import Faker
from db.connection import get_connection
from data.references import get_reviews_reference_data  
from utils import generate_timestamps_list
import random

faker = Faker()
Faker.seed(43)
random.seed(43)

def generate_reviews(ref_data, max_reviews_per_user=3, reply_ratio=0.25, inactive_ratio=0.05, delete_ratio=0.1):
    reviews = []

    users = ref_data.get("users")
    order_items = ref_data.get("order_items")  

    if not users or not order_items:
        raise ValueError("Reference data for users or orders is missing")

    user_products = {}
    for oi in order_items:
        uid = oi['user_id']  
        pid = oi['product_id']
        user_products.setdefault(uid, []).append(pid)

    all_reviews = []

    for user in users:
        user_id = user['user_id']
        purchased_products = list(set(user_products.get(user_id, [])))  
        if not purchased_products:
            continue

        num_reviews = min(len(purchased_products), random.randint(1, max_reviews_per_user))
        timestamps = generate_timestamps_list(num_reviews)
        product_sample = random.sample(purchased_products, num_reviews)

        for i, product_id in enumerate(product_sample):
            created_at, updated_at = timestamps[i]

            valid_replies = [r for r in all_reviews if r["product_id"] == product_id]
            parent_review_id = None
            if valid_replies and random.random() < reply_ratio:
                parent_review_id = random.choice(valid_replies).get("review_id")

            review = {
                "review_id": len(all_reviews) + 1,
                "user_id": user_id,
                "parent_review_id": parent_review_id,
                "product_id": product_id,
                "review_text": faker.paragraph(nb_sentences=random.randint(1, 3)),
                "is_delete": random.random() < delete_ratio,
                "is_active": random.random() > inactive_ratio,
                "created_at": created_at,
                "updated_at": updated_at,
            }

            all_reviews.append(review)
            reviews.append({k: v for k, v in review.items() if k != "review_id"})

    return reviews

def insert_reviews(reviews):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO reviews (
            user_id, parent_review_id, product_id, review_text,
            is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(user_id)s, %(parent_review_id)s, %(product_id)s, %(review_text)s,
            %(is_delete)s, %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, reviews)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(reviews)} fake reviews inserted.")


if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reviews_reference_data(conn)  

    reviews = generate_reviews(ref_data)
    insert_reviews(reviews)
