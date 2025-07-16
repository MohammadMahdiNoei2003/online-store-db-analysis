\connect onlinestore;

INSERT INTO order_statuses (order_status_id, status, is_delete, is_active, created_at, updated_at)
VALUES
(1, 'pending', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'confirmed', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'processing', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 'shipped', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, 'delivered', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, 'canceled', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(7, 'returned', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (order_status_id) DO NOTHING;