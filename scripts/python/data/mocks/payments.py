from faker import Faker
import random
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps

fake = Faker()
Faker.seed(42)
random.seed(42)

NULL_RATIO = 0.05  

def maybe_null(value_list, key):
    return None if random.random() < NULL_RATIO else random.choice(value_list)[key]

def generate_payments(ref_data, inactive_ratio=0.05, delete_ratio=0.01):
    payments = []

    users = ref_data.get("users")
    payment_methods = ref_data.get("payment_methods")
    payment_statuses = ref_data.get("payment_statuses")
    banks = ref_data.get("banks")

    if not users or not payment_methods or not payment_statuses or not banks:
        raise ValueError("Referense data for users, payment methods, payment statuses and banks is missing")
    
    possible_counts = list(range(0, 11))
    weights = [8, 10, 12, 12, 10, 9, 6, 4, 3, 2, 1]

    for user in users:
        num_payments = random.choices(possible_counts, weights=weights, k=1)[0]
        
        for _ in range(num_payments):
            created_at, updated_at = generate_timestamps(3)

            payments.append({
                "user_id": user['user_id'],
                "payment_method_id": maybe_null(payment_methods, 'payment_method_id'),
                "payment_status_id": maybe_null(payment_statuses, 'payment_status_id'),
                "bank_id": maybe_null(banks, 'bank_id'),
                "transaction_id": fake.uuid4(),
                "payment_date": created_at,
                "payment_amount": round(random.uniform(10, 10000), 2),
                "is_delete": random.random() < delete_ratio,
                "is_active": random.random() > inactive_ratio,
                "created_at": created_at,
                "updated_at": updated_at,
            })
    
    return payments

def insert_payments(payments):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO payments (
            user_id, payment_method_id, payment_status_id, bank_id, 
            transaction_id, payment_date, payment_amount, 
            is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(user_id)s, %(payment_method_id)s, %(payment_status_id)s, %(bank_id)s, 
            %(transaction_id)s, %(payment_date)s, %(payment_amount)s, 
            %(is_delete)s, %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, payments)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(payments)} fake payments inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    payments = generate_payments(ref_data)
    insert_payments(payments)