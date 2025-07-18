from faker import Faker
from db.connection import get_connection
from data.references import get_reference_data
from utils import generate_timestamps_list
import random

faker = Faker()
Faker.seed(42)
random.seed(42)

CATEGORY_ATTRIBUTES = {
    "Electronics": ["Brand", "Model", "Power", "Voltage", "Warranty"],
    "Home & Kitchen": ["Material", "Color", "Capacity", "Weight", "Dimensions"],
    "Fashion": ["Size", "Color", "Material", "Brand", "Gender"],
    "Health & Personal Care": ["Volume", "Ingredients", "Skin Type", "Usage"],
    "Sports & Outdoors": ["Weight", "Material", "Dimensions", "Color"],
    "Books": ["Author", "Publisher", "Language", "Pages"],
    "Toys & Games": ["Age Range", "Material", "Color", "Dimensions"],
    "Office Supplies": ["Color", "Material", "Brand", "Dimensions"],
    "Automotive": ["Brand", "Model", "Compatibility", "Power"],
    "Beauty & Cosmetics": ["Shade", "Skin Type", "Volume", "Ingredients"],
    "Pet Supplies": ["Animal Type", "Material", "Weight", "Brand"],
    "Groceries": ["Weight", "Brand", "Expiration Date", "Ingredients"],
    "Baby Products": ["Age Range", "Material", "Color", "Safety Certification"],
    "Tools & Hardware": ["Material", "Power", "Voltage", "Usage"],
    "Garden & Outdoor": ["Material", "Dimensions", "Color", "Usage"],
    "Jewelry": ["Material", "Color", "Weight", "Gem Type"],
    "Musical Instruments": ["Type", "Brand", "Material", "Dimensions"],
    "Footwear": ["Size", "Color", "Material", "Gender"],
    "Mobile Accessories": ["Brand", "Compatibility", "Color", "Type"],
    "Computer & Accessories": ["Brand", "Model", "Compatibility", "Power"],
}

def get_attribute_name_to_id_map(ref_data):
    attributes = ref_data.get("product_attributes")
    if not attributes:
        raise ValueError("No product attributes found in reference data")
    
    return {attr['name']: attr['product_attribute_id'] for attr in attributes}

def generate_attribute_value(attribute_name):
    if attribute_name in ["Brand", "Model", "Author", "Publisher", "Type", "Shade", "Gem Type", "Compatibility", "Usage", "Skin Type"]:
        return faker.word()
    if attribute_name in ["Power", "Voltage", "Capacity", "Weight", "Volume", "Size", "Pages"]:
        return str(random.randint(1, 1000))
    if attribute_name == "Color":
        return faker.color_name()
    if attribute_name == "Dimensions":
        return f"{random.randint(1, 100)}x{random.randint(1, 100)}x{random.randint(1, 100)} cm"
    if attribute_name in ["Warranty", "Expiration Date", "Safety Certification", "Age Range"]:
        return f"{random.randint(1, 5)} years"
    if attribute_name == "Ingredients":
        return " ".join(faker.words(nb=3, unique=True))
    if attribute_name == "Gender":
        return random.choice(["Male", "Female", "Unisex"])
    if attribute_name == "Animal Type":
        return random.choice(["Dog", "Cat", "Bird", "Fish"])
    return faker.word()

def generate_product_attribute_values(ref_data):
    conn = get_connection()
    attribute_map = get_attribute_name_to_id_map(ref_data)
    
    products = ref_data.get("products")
    categories = ref_data.get("categories")
    
    if not products or not categories:
        raise ValueError("Reference data for products or categories is missing")

    categories_map = {cat['category_id']: cat['name'] for cat in categories}

    timestamps = generate_timestamps_list(len(products)*5)  
    idx = 0
    records = []

    for product in products:
        product_id = product["product_id"]
        category_id = product.get("category_id")
        category_name = categories_map.get(category_id)

        if not category_name or category_name not in CATEGORY_ATTRIBUTES:
            continue

        attributes_for_category = CATEGORY_ATTRIBUTES[category_name]

        for attr_name in attributes_for_category:
            attribute_id = attribute_map.get(attr_name)
            if not attribute_id:
                continue
            value = generate_attribute_value(attr_name)

            created_at, updated_at = timestamps[idx]
            idx += 1

            records.append({
                "product_id": product_id,
                "attribute_id": attribute_id,
                "value": value if isinstance(value, str) else " ".join(value) if isinstance(value, list) else str(value),
                "is_delete": False,
                "is_active": True,
                "created_at": created_at,
                "updated_at": updated_at,
            })

    conn.close()
    return records


def insert_product_attribute_values(records):
    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO product_attribute_values (
            product_id, attribute_id, value, is_delete, is_active, created_at, updated_at
        ) VALUES (
            %(product_id)s, %(attribute_id)s, %(value)s, %(is_delete)s, %(is_active)s, %(created_at)s, %(updated_at)s
        )
    """

    cursor.executemany(insert_query, records)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(records)} fake product attribute values inserted.")

if __name__ == "__main__":
    conn = get_connection()
    ref_data = get_reference_data(conn)
    conn.close()

    records = generate_product_attribute_values(ref_data)
    insert_product_attribute_values(records)
