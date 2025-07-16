\connect onlinestore;

INSERT INTO payment_methods (payment_method_id, method, is_delete, is_active, created_at, updated_at)
VALUES
(1, 'credit_card', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'debit_card', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'cash_on_delivery', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, 'bank_transfer', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (payment_method_id) DO NOTHING;