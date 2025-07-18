from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps_list
import random

faker = Faker()
Faker.seed(42)
random.seed(42)

def generate_product_images(ref_data, max_image_per_product=4):
    images = []

    products = ref_data.get("products");

    if not products:
        raise ValueError("Reference data for products is missing")

    for product in products:
        product_id = product["product_id"]
        num_images = random.randint(1, max_image_per_product)
        main_index = random.randint(0, num_images - 1)

        timstamps = generate_timestamps_list(num_images)

        for i in range(num_images):
            is_main = i == main_index
            created_at, updated_at = timstamps[i]

            images.append({
                "product_id": product_id,
                "image_url": f"https://picsum.photos/seed/{faker.uuid4()}/600/400",
                "is_main": is_main,
                "display_order": i,
                "is_delete": random.choices([False, True], weights=[90, 10])[0],
                "is_active": random.choices([True, False], weights=[95, 5])[0],
                "created_at": created_at,
                "updated_at": updated_at,
            })

    return images

def insert_product_images(images):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO product_images (
            product_id, image_url, is_main, display_order, 
            is_delete, is_active, created_at, updated_at
        )
        VALUES (
            %(product_id)s, %(image_url)s, %(is_main)s,
            %(display_order)s, %(is_delete)s, %(is_active)s,
            %(created_at)s, %(updated_at)s 
        )
    """

    cursor.executemany(insert_query, images)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(images)} fake product images inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)

    images = generate_product_images(ref_data)
    insert_product_images(images)