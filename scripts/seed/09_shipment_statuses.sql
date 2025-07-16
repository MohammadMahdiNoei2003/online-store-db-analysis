\connect onlinestore;

INSERT INTO shipment_statuses (shipment_status_id, status, is_delete, is_active, created_at, updated_at)
VALUES
(1, 'pending', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'in_transit', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'out_for_delivery', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 'delivered', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, 'canceled', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, 'failed_delivery', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (shipment_status_id) DO NOTHING;