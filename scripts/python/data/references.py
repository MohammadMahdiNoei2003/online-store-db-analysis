import psycopg2

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
    }

    reference_data = {}

    with conn.cursor() as cursor:
        for key, (fields, table) in tables.items():
            query = f"SELECT {fields} FROM {table} WHERE is_delete = FALSE AND is_active = TRUE;"
            cursor.execute(query)
            reference_data[key] = cursor.fetchall()

    return reference_data
