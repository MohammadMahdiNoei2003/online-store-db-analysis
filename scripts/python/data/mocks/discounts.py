from faker import Faker
from db.connection import get_connection
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_discounts(num_discounts=350, years_span=3):
    discounts = []
    base_date = datetime.now()
    start_limit = base_date - timedelta(days=365*years_span)

    for _ in range(num_discounts):
        started_at = start_limit + timedelta(days=random.randint(0, 365*years_span))
        
        duration_days = random.randint(1, 90)
        expired_at = started_at + timedelta(days=duration_days)
        
        percentage = round(random.uniform(5, 70), 2)
        
        discounts.append({
            "percentage": percentage,
            "started_at": started_at,
            "expired_at": expired_at,
        })
    return discounts

def insert_discounts(discounts):
    conn = get_connection()
    cursor = conn.cursor()
    
    insert_query = """
        INSERT INTO discounts (percentage, started_at, expired_at)
        VALUES (%(percentage)s, %(started_at)s, %(expired_at)s)
    """
    cursor.executemany(insert_query, discounts)
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"{len(discounts)} discounts inserted.")

if __name__ == "__main__":
    discounts = generate_discounts()
    insert_discounts(discounts)
