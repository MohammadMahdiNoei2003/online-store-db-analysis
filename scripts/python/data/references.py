import psycopg2
import psycopg2.extras

def get_reference_data(conn):
    tables = {
        # reference tables
        "genders": ("gender_id, gender", "genders"),
        "roles": ("role_id, role_title", "roles"),
        "provinces": ("province_id, name", "provinces"),
        "address_types": ("address_type_id, type", "address_types"),
        "banks": ("bank_id, name", "banks"),
        "payment_methods": ("payment_method_id, method", "payment_methods"),
        "payment_statuses": ("payment_status_id, status", "payment_statuses"),
        "shipment_methods": ("shipment_method_id, method, transport_company_name", "shipment_methods"),
        "shipment_statuses": ("shipment_status_id, status", "shipment_statuses"),
        "order_statuses": ("order_status_id, status", "order_statuses"),

        # non rerference tables
        "users": ("user_id", "users"),
        "cities": ("city_id", "cities"),
        "categories": ("category_id, name", "categories"),
        "products": ("product_id, category_id", "products"),
        "product_attributes": ("product_attribute_id, name", "product_attributes"),
        "brands": ("brand_id", "brands"),
        "discounts": ("discount_id, expired_at", "discounts"),
        "carts": ("cart_id", "carts"),
        "payments": ("payment_id, user_id, payment_amount", "payments"),
        "shipments": ("shipment_id, user_id", "shipments"),
        "orders": ("order_id", "orders"),
    }

    reference_data = {}

    with conn.cursor() as cursor:
        for key, (fields, table) in tables.items():
            if key == "discounts":
                query = f"SELECT {fields} FROM {table};"
            else:
                query = f"SELECT {fields} FROM {table} WHERE is_delete = FALSE AND is_active = TRUE;"
            cursor.execute(query)
            reference_data[key] = cursor.fetchall()

    return reference_data

def get_reviews_reference_data(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute("SELECT user_id FROM users WHERE is_delete = FALSE AND is_active = TRUE;")
        users_rows = cursor.fetchall()
        users = [{"user_id": row['user_id']} for row in users_rows]

        cursor.execute("""
            SELECT oi.order_item_id, o.user_id, oi.product_id 
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            WHERE oi.is_delete = FALSE AND oi.is_active = TRUE
              AND o.is_delete = FALSE AND o.is_active = TRUE;
        """)
        order_items_rows = cursor.fetchall()
        order_items = [
            {
                "order_item_id": row['order_item_id'],
                "user_id": row['user_id'],
                "product_id": row['product_id']
            } for row in order_items_rows
        ]

    return {
        "users": users,
        "order_items": order_items
    }

