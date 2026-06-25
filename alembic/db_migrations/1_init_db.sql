BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> a71a738c2829

CREATE TABLE room (
    id SERIAL NOT NULL, 
    name VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (id), 
    UNIQUE (name)
);

CREATE TABLE "user" (
    id SERIAL NOT NULL, 
    username VARCHAR NOT NULL, 
    hashed_password VARCHAR NOT NULL,
    is_admin BOOLEAN, 
    PRIMARY KEY (id), 
    UNIQUE (id), 
    UNIQUE (username)
);

CREATE TABLE slot (
    id SERIAL NOT NULL, 
    start_time TIME WITHOUT TIME ZONE NOT NULL, 
    end_time TIME WITHOUT TIME ZONE NOT NULL, 
    slot_date DATE NOT NULL, 
    room_id INTEGER NOT NULL,
    PRIMARY KEY (id), 
    CONSTRAINT check_slot_times CHECK (end_time > start_time), 
    FOREIGN KEY(room_id) REFERENCES room (id) ON DELETE CASCADE,
    UNIQUE (id)
);

CREATE TABLE reservation (
    id SERIAL NOT NULL, 
    user_id INTEGER NOT NULL,
    slot_id INTEGER NOT NULL,
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES "user" (id) ON DELETE CASCADE,
    FOREIGN KEY(slot_id) REFERENCES slot (id) ON DELETE CASCADE,
    UNIQUE (id),
    UNIQUE (slot_id)
);

INSERT INTO alembic_version (version_num) VALUES ('a71a738c2829') RETURNING alembic_version.version_num;

COMMIT;

