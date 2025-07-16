\connect onlinestore;

INSERT INTO shipment_methods (shipment_method_id, method, transport_company_name, is_delete, is_active, created_at, updated_at)
VALUES
(1, 'standard_post', 'Iran Post', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'express_post', 'Iran Post', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'fast_post', 'Tipax', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 'courier', 'SnappBox', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, 'in_store_pickup', 'N/A', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (shipment_method_id) DO NOTHING;