from faker import Faker
import random
from datetime import timedelta, date
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_product_prices(n, ref_data, inactive_ratio=0.1, delete_ratio=0.05):
    product_prices = []

    products = ref_data.get("products")

    if not products:
        raise ValueError("Reference data for products is missing")
    
    today = date.today()
    start_range = today - timedelta(days=3*365)

    for product in products:
        product_id = product["product_id"]
        current_price = round(random.uniform(50, 5000), 2)
        current_date = start_range

        records = []

        while current_date < today:
            period_days = random.randint(60, 180)
            end_date = current_date + timedelta(days=period_days)
            
            if end_date > today:
                end_date = today

            change = random.uniform(-0.05, 0.15)
            new_price = round(current_price * (1 + change), 2)

            created_at, updated_at = generate_timestamps()

            records.append({
                "product_id": product_id,
                "price": new_price,
                "started_at": current_date,
                "ended_at": end_date,
                "is_active": False,
                "is_delete": random.random() > delete_ratio,
                "created_at": created_at,
                "updated_at": updated_at,
            })
            
            current_price = new_price
            current_date = end_date + timedelta(days=1)
        
        if records:
            records[-1]["is_active"] = True

        product_prices.extend(records)

    return product_prices

def insert_product_prices(product_prices):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO product_prices (
            product_id, price, started_at, ended_at, is_delete, 
            is_active, created_at, updated_at
        )
        VALUES (
            %(product_id)s, %(price)s, %(started_at)s, %(ended_at)s, %(is_delete)s, 
            %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, product_prices)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(product_prices)} fake product prices inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    prices = generate_product_prices(8000, ref_data)
    insert_product_prices(prices)