from faker import Faker
import random
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_addresses(n, ref_data, inactive_ratio=0.1, delete_ratio=0.05):
    addresses = []

    users = ref_data.get("users")
    cities = ref_data.get("cities")
    address_types = ref_data.get("address_types")

    if not users or not cities or not address_types:
        raise ValueError("Reference data for users, cities, or address_types is missing")

    for user in users:
        created_at, updated_at = generate_timestamps(3)

        addresses.append({
            "user_id": user['user_id'],
            "city_id": random.choice(cities)['city_id'],
            "address_type_id": random.choice(address_types)['address_type_id'],
            "address_line": fake.address().replace('\n', ', '),
            "postal_code": fake.postcode(),
            "is_active": random.random() > inactive_ratio,
            "is_delete": random.random() < delete_ratio,
            "created_at": created_at,
            "updated_at": updated_at,
        })

    while len(addresses) < n:
        created_at, updated_at = generate_timestamps(3)
        user = random.choice(users)

        addresses.append({
            "user_id": user['user_id'],
            "city_id": random.choice(cities)['city_id'],
            "address_type_id": random.choice(address_types)['address_type_id'],
            "address_line": fake.address().replace('\n', ', '),
            "postal_code": fake.postcode(),
            "is_active": random.random() > inactive_ratio,
            "is_delete": random.random() < delete_ratio,
            "created_at": created_at,
            "updated_at": updated_at,
        })

    return addresses

def insert_addresses(addresses):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO addresses (
            user_id, city_id, address_type_id,
            address_line, postal_code,
            is_active, is_delete,
            created_at, updated_at
        )
        VALUES (
            %(user_id)s, %(city_id)s, %(address_type_id)s,
            %(address_line)s, %(postal_code)s,
            %(is_active)s, %(is_delete)s,
            %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, addresses)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(addresses)} fake addresses inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    addresses = generate_addresses(3000, ref_data)
    insert_addresses(addresses)
