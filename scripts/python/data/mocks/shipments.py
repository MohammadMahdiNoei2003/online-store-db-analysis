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

def generate_shipments(ref_data, inactive_ratio=0.05, delete_ratio=0.01):
    shipments = []

    users = ref_data.get("users")
    shipment_methods = ref_data.get("shipment_methods")
    shipment_statuses = ref_data.get("shipment_statuses")

    if not users or not shipment_methods or not shipment_statuses:
        raise ValueError("Reference data for users, shipment methods and statuses is missing")

    possible_counts = list(range(0, 11))
    weights = [8, 10, 12, 12, 10, 9, 6, 4, 3, 2, 1]  

    for user in users:
        num_shipments = random.choices(possible_counts, weights=weights, k=1)[0]

        for _ in range(num_shipments):
            created_at, updated_at = generate_timestamps(3)
            shipment_date = created_at
            delivery_deadline = shipment_date + fake.time_delta(end_datetime="+10d")
            shipment_cost = round(random.uniform(20, 5000), 2)

            shipments.append({
                "user_id": user['user_id'],
                "shipment_method_id": maybe_null(shipment_methods, 'shipment_method_id'),
                "shipment_status_id": maybe_null(shipment_statuses, 'shipment_status_id'),
                "tracking_code": fake.uuid4(),
                "shipment_date": shipment_date,
                "shipment_cost": shipment_cost,
                "delivery_deadline": delivery_deadline,
                "is_delete": random.random() < delete_ratio,
                "is_active": random.random() > inactive_ratio,
                "created_at": created_at,
                "updated_at": updated_at,
            })

    return shipments

def insert_shipments(shipments):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO shipments (
            user_id, shipment_method_id, shipment_status_id,
            tracking_code, shipment_date, shipment_cost, delivery_deadline,
            is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(user_id)s, %(shipment_method_id)s, %(shipment_status_id)s,
            %(tracking_code)s, %(shipment_date)s, %(shipment_cost)s, %(delivery_deadline)s,
            %(is_delete)s, %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, shipments)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(shipments)} fake shipments inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    shipments = generate_shipments(ref_data)
    insert_shipments(shipments)
