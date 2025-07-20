#!/bin/bash
set -e

# Wait for Postgres to be ready
echo "Waiting for postgres to be ready..."
until psql "host=db port=5432 user=$POSTGRES_USER password=$POSTGRES_PASSWORD dbname=$POSTGRES_DB" -c '\q' 2>/dev/null
do
  echo "Postgres is unavailable - sleeping"
  sleep 2
done

echo "Postgres is up. Waiting for reference data to be available..."

function wait_for_table_data() {
  local table=$1
  echo "DEBUG: Checking table $table data..."
  until psql "host=db port=5432 user=$POSTGRES_USER password=$POSTGRES_PASSWORD dbname=$POSTGRES_DB" -tAc "SELECT 1 FROM $table LIMIT 1;" | grep -q 1
  do
    echo "⏳ Waiting for data in ${table}..."
    sleep 2
  done
  echo "✅ Data available in ${table}"
}


wait_for_table_data "genders"
wait_for_table_data "provinces"
wait_for_table_data "address_types"
wait_for_table_data "roles"
wait_for_table_data "order_statuses"
wait_for_table_data "payment_methods"
wait_for_table_data "payment_statuses"
wait_for_table_data "shipment_methods"
wait_for_table_data "shipment_statuses"
wait_for_table_data "banks"

echo "All reference tables are ready. Starting data load..."

export PYTHONPATH=/app

python data/mocks/users.py
python data/mocks/user_roles.py
python data/mocks/cities.py
python data/mocks/addresses.py
python data/mocks/categories.py
python data/mocks/products.py
python data/mocks/product_prices.py
python data/mocks/product_images.py
python data/mocks/product_attributes.py
python data/mocks/product_attribute_values.py
python data/mocks/brands.py
python data/mocks/product_brands.py
python data/mocks/discounts.py
python data/mocks/product_discounts.py
python data/mocks/category_discounts.py
python data/mocks/payments.py
python data/mocks/shipments.py
python data/mocks/carts.py
python data/mocks/cart_items.py
python data/mocks/orders.py
python data/mocks/order_items.py
python data/mocks/wishlists.py
python data/mocks/ratings.py
python data/mocks/reviews.py

echo "Data load completed."

exit 0
