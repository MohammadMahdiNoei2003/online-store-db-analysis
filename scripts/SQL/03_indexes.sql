-- Online Store Indexes: PostgreSQL Standard

-- =============================
-- INDEXES SETUP
-- =============================

CREATE INDEX idx_users_gender_id ON users(gender_id);
CREATE INDEX idx_users_email ON users(email_address);
CREATE INDEX idx_users_national_code ON users(national_code);

CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);

CREATE INDEX idx_cities_province_id ON cities(province_id);

CREATE INDEX idx_addresses_user_id ON addresses(user_id);
CREATE INDEX idx_addresses_city_id ON addresses(city_id);
CREATE INDEX idx_addresses_address_type_id ON addresses(address_type_id);

CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_sku ON products(sku);

CREATE INDEX idx_product_prices_product_id ON product_prices(product_id);

CREATE INDEX idx_product_images_product_id ON product_images(product_id);

CREATE INDEX idx_product_attribute_values_product_id ON product_attribute_values(product_id);
CREATE INDEX idx_product_attribute_values_attribute_id ON product_attribute_values(attribute_id);

CREATE INDEX idx_product_brands_product_id ON product_brands(product_id);
CREATE INDEX idx_product_brands_brand_id ON product_brands(brand_id);

CREATE INDEX idx_product_discounts_product_id ON product_discounts(product_id);
CREATE INDEX idx_product_discounts_discount_id ON product_discounts(discount_id);

CREATE INDEX idx_category_discounts_category_id ON category_discounts(category_id);
CREATE INDEX idx_category_discounts_discount_id ON category_discounts(discount_id);

CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_payments_method_id ON payments(payment_method_id);
CREATE INDEX idx_payments_status_id ON payments(payment_status_id);
CREATE INDEX idx_payments_bank_id ON payments(bank_id);

CREATE INDEX idx_shipments_user_id ON shipments(user_id);
CREATE INDEX idx_shipments_method_id ON shipments(shipment_method_id);
CREATE INDEX idx_shipments_status_id ON shipments(shipment_status_id);

CREATE INDEX idx_carts_user_id ON carts(user_id);

CREATE INDEX idx_cart_items_cart_id ON cart_items(cart_id);
CREATE INDEX idx_cart_items_product_id ON cart_items(product_id);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_payment_id ON orders(payment_id);
CREATE INDEX idx_orders_shipment_id ON orders(shipment_id);
CREATE INDEX idx_orders_status_id ON orders(order_status_id);
CREATE INDEX idx_orders_created_at ON orders(created_at);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

CREATE INDEX idx_wishlists_user_id ON wishlists(user_id);
CREATE INDEX idx_wishlists_product_id ON wishlists(product_id);

CREATE INDEX idx_ratings_user_id ON ratings(user_id);
CREATE INDEX idx_ratings_product_id ON ratings(product_id);

CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_product_id ON reviews(product_id);
CREATE INDEX idx_reviews_parent_id ON reviews(parent_review_id);