from faker import Faker
import random
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps

fake = Faker()
random.seed(42)
Faker.seed(42)

def generate_cities(n, ref_data, inactive_ratio=0.1, delete_ratio=0.05):
    cities = []
    provinces = ref_data.get("provinces", [])

    if not provinces:
        raise Exception("Provinces reference data is empty!")

    for _ in range(n):
        created_at, updated_at = generate_timestamps(3)
         
        cities.append({
            "province_id": random.choice(provinces)['province_id'],  
            "name": fake.city(),
            "is_active": random.random() > inactive_ratio,
            "is_delete": random.random() < delete_ratio,
            "created_at": created_at,
            "updated_at": updated_at
        })
    return cities

def insert_cities(cities):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO cities (
            province_id, name, is_active, is_delete, created_at, updated_at
        )
        VALUES (
            %(province_id)s, %(name)s, %(is_active)s, %(is_delete)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, cities)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(cities)} fake cities inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)
    cities = generate_cities(300, ref_data)  
    insert_cities(cities)
