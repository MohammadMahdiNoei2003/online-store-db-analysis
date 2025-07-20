from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data  
from utils import generate_timestamps
import random

faker = Faker()
Faker.seed(42)
random.seed(42)

def generate_user_roles(ref_data, num_admins=3, inactive_ratio=0.2, delete_ratio=0.1):
    users = ref_data.get("users")
    roles = ref_data.get("roles")

    if not users or not roles:
        raise ValueError("Reference data for users or roles is missing")

    admin_role_id = None
    customer_role_id = None
    for role in roles:
        if role.get("role_title") == "admin":
            admin_role_id = role.get("role_id")
        elif role.get("role_title") == "customer":
            customer_role_id = role.get("role_id")

    if admin_role_id is None or customer_role_id is None:
        raise ValueError("Admin or Customer role not found in roles data")

    user_roles = []
    all_user_ids = [user["user_id"] for user in users]

    num_admins = min(num_admins, len(all_user_ids))
    admin_user_ids = random.sample(all_user_ids, num_admins)

    for user_id in all_user_ids:
        role_id = admin_role_id if user_id in admin_user_ids else customer_role_id
        created_at, updated_at = generate_timestamps(3)

        user_role = {
            "user_id": user_id,
            "role_id": role_id,
            "is_delete": random.random() < delete_ratio,
            "is_active": random.random() > inactive_ratio,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        user_roles.append(user_role)

    return user_roles

def insert_user_roles(user_roles):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO user_roles (
            user_id, role_id, is_delete, is_active, created_at, updated_at
        ) VALUES (
            %(user_id)s, %(role_id)s, %(is_delete)s, %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    for ur in user_roles:
        cursor.execute("""
            SELECT 1 FROM user_roles
            WHERE user_id = %s AND role_id = %s
            LIMIT 1
        """, (ur["user_id"], ur["role_id"]))

        if cursor.fetchone() is None:
            cursor.execute(insert_query, ur)
        else:
            print(f"Duplicate record found for user_id={ur['user_id']} and role_id={ur['role_id']}, skipping insertion.")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(user_roles)} records inserted into user_roles.")


if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)  

    user_roles = generate_user_roles(ref_data, num_admins=3)
    insert_user_roles(user_roles)
