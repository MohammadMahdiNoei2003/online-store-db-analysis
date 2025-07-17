from faker import Faker
import random
import hashlib
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_users(n, ref_data, inactive_ratio=0.1, delete_ratio=0.05):
    users = []

    for _ in range(n):
        password = fake.password()
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        created_at, updated_at  = generate_timestamps(3)

        users.append({
            "gender_id": random.choice(ref_data["genders"])['gender_id'],
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "national_code": str(fake.unique.random_number(digits=10)).zfill(10),
            "email_address": fake.unique.email(),
            "phone_number": fake.phone_number()[:20],
            "dob": fake.date_of_birth(minimum_age=15, maximum_age=70),
            "password_hash": password_hash,
            "profile_img_url": fake.image_url(),
            "is_active": random.random() > inactive_ratio,
            "is_delete": random.random() < delete_ratio,
            "created_at": created_at,
            "updated_at": updated_at,
        })
    return users

def insert_users(users):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO users (
            gender_id, first_name, last_name, national_code,
            email_address, phone_number, dob, password_hash,
            profile_img_url, is_active, is_delete,
            created_at, updated_at
        )
        VALUES (
            %(gender_id)s, %(first_name)s, %(last_name)s, %(national_code)s,
            %(email_address)s, %(phone_number)s, %(dob)s, %(password_hash)s,
            %(profile_img_url)s, %(is_active)s, %(is_delete)s,
            %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, users)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(users)} fake users inserted.")

if __name__ == "__main__":
    ref_data = get_reference_data(get_connection())
    users = generate_users(1000, ref_data)
    insert_users(users)
