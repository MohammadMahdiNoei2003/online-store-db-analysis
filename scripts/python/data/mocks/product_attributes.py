from faker import Faker
from db.connection import get_connection
from utils import generate_timestamps_list

faker = Faker()
Faker.seed(42)

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

def get_unique_attributes():
    all_attributes = set()
    for attribute in CATEGORY_ATTRIBUTES.values():
        all_attributes.update(attribute)
    return list(all_attributes)

def insert_product_attributes(attributes):
    conn = get_connection()
    cursor = conn.cursor()

    timestamps = generate_timestamps_list(len(attributes))
    records = []
    for i, attr in enumerate(attributes):
        created_at, updated_at = timestamps[i]
        is_delete = False
        is_active = True
        records.append((attr, is_delete, is_active, created_at, updated_at))

    cursor.executemany("""
        INSERT INTO product_attributes (name, is_delete, is_active, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s) 
    """, records)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    unique_attributes = get_unique_attributes()
    insert_product_attributes(unique_attributes)
    print(f"{len(unique_attributes)} unique product attributes inserted.")