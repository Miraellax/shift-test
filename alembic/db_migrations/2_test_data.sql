BEGIN;

INSERT INTO "user" (username,
                    hashed_password,
                    is_admin) VALUES
    ('Test_1', '$argon2id$v=19$m=65536,t=3,p=4$1V9YeoZGda722cTIfTCBTg$uAmhPLz7HTBUZ3jVtiTtR07Tl5u5ju16qYjz7uN0cgI', FALSE),
    ('Test_2', '$argon2id$v=19$m=65536,t=3,p=4$TLF1RWsthUrVIyREzAmnoQ$HV3POx5YAcKjskOLd3BnmzLRF2JOZc+gN1RNw4NETE8', FALSE),
    ('Test_3_admin', '$argon2id$v=19$m=65536,t=3,p=4$OmVpgSZr7XyRcpoqWyIU5g$0Tx2+PwKa0jiXt6uyJIrPjN+MMzbYAr3TANF3Q9U6Fk', TRUE);

INSERT INTO "room" (name) VALUES
    ('Test_room_1'),
    ('Test_room_2'),
    ('Test_room_3');

WITH temp_room_id AS (SELECT id FROM "room" WHERE room.name = 'Test_room_1')
    INSERT INTO "slot" (start_time,
                        end_time,
                        slot_date,
                        room_id) VALUES
        ('10:00', '10:50', '2026-06-18', (SELECT id FROM temp_room_id)),
        ('11:00', '11:50', '2026-06-18', (SELECT id FROM temp_room_id)),
        ('12:00', '12:50', '2026-06-18', (SELECT id FROM temp_room_id)),
        ('13:00', '13:50', '2026-06-18', (SELECT id FROM temp_room_id));

WITH temp_room_id AS (SELECT id FROM "room" WHERE room.name = 'Test_room_2')
    INSERT INTO "slot" (start_time,
                        end_time,
                        slot_date,
                        room_id) VALUES
        ('10:00', '10:50', '2026-06-18', (SELECT id FROM temp_room_id)),
        ('11:00', '11:50', '2026-06-18', (SELECT id FROM temp_room_id)),
        ('12:00', '12:50', '2026-06-18', (SELECT id FROM temp_room_id)),
        ('13:00', '13:50', '2026-06-18', (SELECT id FROM temp_room_id));

WITH temp_room_id AS (SELECT id FROM "room" WHERE room.name = 'Test_room_3')
    INSERT INTO "slot" (start_time,
                        end_time,
                        slot_date,
                        room_id) VALUES
        ('10:00', '10:50', '2026-06-19', (SELECT id FROM temp_room_id)),
        ('11:00', '11:50', '2026-06-19', (SELECT id FROM temp_room_id)),
        ('12:00', '12:50', '2026-06-19', (SELECT id FROM temp_room_id)),
        ('13:00', '13:50', '2026-06-19', (SELECT id FROM temp_room_id));


WITH temp_room_id AS (SELECT id FROM "room" WHERE room.name = 'Test_room_1'),
     temp_user_id AS (SELECT id FROM "user" WHERE "user".username = 'Test_1'),
	 temp_slot_id AS (SELECT id FROM "slot" WHERE ("slot".start_time = '10:00' AND "slot".room_id = (SELECT id FROM temp_room_id)))
    INSERT INTO "reservation" (user_id,
                               slot_id) VALUES
        ((SELECT id FROM temp_user_id),  (SELECT id FROM temp_slot_id));

WITH temp_room_id AS (SELECT id FROM "room" WHERE room.name = 'Test_room_1'),
     temp_user_id AS (SELECT id FROM "user" WHERE "user".username = 'Test_1'),
	 temp_slot_id AS (SELECT id FROM "slot" WHERE ("slot".start_time = '11:00' AND "slot".room_id = (SELECT id FROM temp_room_id)))
    INSERT INTO "reservation" (user_id,
                               slot_id) VALUES
        ((SELECT id FROM temp_user_id),  (SELECT id FROM temp_slot_id));

WITH temp_room_id AS (SELECT id FROM "room" WHERE room.name = 'Test_room_1'),
     temp_user_id AS (SELECT id FROM "user" WHERE "user".username = 'Test_2'),
	 temp_slot_id AS (SELECT id FROM "slot" WHERE ("slot".start_time = '12:00' AND "slot".room_id = (SELECT id FROM temp_room_id)))
    INSERT INTO "reservation" (user_id,
                               slot_id) VALUES
        ((SELECT id FROM temp_user_id),  (SELECT id FROM temp_slot_id));

WITH temp_room_id AS (SELECT id FROM "room" WHERE room.name = 'Test_room_2'),
     temp_user_id AS (SELECT id FROM "user" WHERE "user".username = 'Test_2'),
	 temp_slot_id AS (SELECT id FROM "slot" WHERE ("slot".start_time = '10:00' AND "slot".room_id = (SELECT id FROM temp_room_id)))
    INSERT INTO "reservation" (user_id,
                               slot_id) VALUES
        ((SELECT id FROM temp_user_id),  (SELECT id FROM temp_slot_id));

WITH temp_room_id AS (SELECT id FROM "room" WHERE room.name = 'Test_room_2'),
     temp_user_id AS (SELECT id FROM "user" WHERE "user".username = 'Test_2'),
	 temp_slot_id AS (SELECT id FROM "slot" WHERE ("slot".start_time = '11:00' AND "slot".room_id = (SELECT id FROM temp_room_id)))
    INSERT INTO "reservation" (user_id,
                               slot_id) VALUES
        ((SELECT id FROM temp_user_id),  (SELECT id FROM temp_slot_id));

WITH temp_room_id AS (SELECT id FROM "room" WHERE room.name = 'Test_room_3'),
     temp_user_id AS (SELECT id FROM "user" WHERE "user".username = 'Test_3_admin'),
	 temp_slot_id AS (SELECT id FROM "slot" WHERE ("slot".start_time = '10:00' AND "slot".room_id = (SELECT id FROM temp_room_id)))
    INSERT INTO "reservation" (user_id,
                               slot_id) VALUES
        ((SELECT id FROM temp_user_id),  (SELECT id FROM temp_slot_id));

WITH temp_room_id AS (SELECT id FROM "room" WHERE room.name = 'Test_room_3'),
     temp_user_id AS (SELECT id FROM "user" WHERE "user".username = 'Test_3_admin'),
	 temp_slot_id AS (SELECT id FROM "slot" WHERE ("slot".start_time = '11:00' AND "slot".room_id = (SELECT id FROM temp_room_id)))
    INSERT INTO "reservation" (user_id,
                               slot_id) VALUES
        ((SELECT id FROM temp_user_id),  (SELECT id FROM temp_slot_id));

COMMIT;

