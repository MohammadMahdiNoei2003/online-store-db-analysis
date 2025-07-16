\connect onlinestore;

INSERT INTO roles (role_id, role_title, is_delete, is_active, created_at, updated_at)
VALUES
(1, 'admin', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'customer', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (role_id) DO NOTHING;
