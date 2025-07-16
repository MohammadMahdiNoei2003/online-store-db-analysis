\connect onlinestore;

INSERT INTO genders (gender_id, gender, is_delete, is_active, created_at, updated_at)
VALUES
(1, 'Male', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, 'Female', FALSE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (gender_id) DO NOTHING;