from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps
import random

faker = Faker()
Faker.seed(42)
random.seed(42)


def generate_orders(ref_data, inactive_ratio=0.15, delete_ratio=0.07, max_orders_per_user=5):
    orders = []

    users = ref_data.get("users")
    payments = ref_data.get("payments")
    shipments = ref_data.get("shipments")
    order_statuses = ref_data.get("order_statuses")

    if not users or not payments or not shipments or not order_statuses:
        raise ValueError("Reference data for users, payments, shipments or order statuses is missing")
    
    payments_by_user = {}
    for payment in payments:
        uid = payment["user_id"]
        payments_by_user.setdefault(uid, []).append(payment)

    shipments_by_user = {}
    for shipment in shipments:
        uid = shipment["user_id"]
        shipments_by_user.setdefault(uid, []).append(shipment)

    for user in users:
        user_id = user['user_id']
        num_orders = random.randint(1, max_orders_per_user)

        for _ in range(num_orders):
            created_at, updated_at = generate_timestamps(3)

            user_payments = payments_by_user.get(user_id, [])
            user_shipments = shipments_by_user.get(user_id, [])

            orders.append({
                "user_id": user_id,
                "payment_id": random.choice(user_payments)['payment_id'] if user_payments and random.random() > 0.1 else None,
                "shipment_id": random.choice(user_shipments)['shipment_id'] if user_shipments and random.random() > 0.15 else None,
                "order_status_id": random.choice(order_statuses)['order_status_id'],
                "order_date": created_at,
                "total_amount": round(random.uniform(10, 1000), 2),  
                "is_delete": random.random() < delete_ratio,
                "is_active": random.random() > inactive_ratio,
                "created_at": created_at,
                "updated_at": updated_at,
            })
    
    return orders

def insert_orders(orders):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO orders (
            user_id, payment_id, shipment_id, order_status_id, 
            order_date, total_amount, is_delete, is_active,
            created_at, updated_at
        )
        VALUES (
            %(user_id)s, %(payment_id)s, %(shipment_id)s, %(order_status_id)s, 
            %(order_date)s, %(total_amount)s, %(is_delete)s, %(is_active)s,
            %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, orders)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(orders)} fake orders inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    orders = generate_orders(ref_data)
    insert_orders(orders)