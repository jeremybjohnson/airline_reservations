CREATE TABLE flights (
    flight_id SERIAL PRIMARY KEY,
    airline varchar(256) NOT NULL,
    flight_number varchar(256) NOT NULL,
    depart_code varchar(3) NOT NULL,
    dest_code varchar(3) NOT NULL,
    depart_date DATE NOT NULL,
    depart_time TIME NOT NULL,
    cost INT NOT NULL,
    avail_seats INT NOT NULL
);

CREATE TABLE users (
    username varchar(255) PRIMARY KEY,
    pass varchar(255) NOT NULL,
    f_name varchar(255) NOT NULL,
    l_name varchar(255) NOT NULL
);

CREATE TABLE reservations (
    reservation_id SERIAL PRIMARY KEY,
    flight_id INT,
    username varchar(255) NOT NULL,
    total_cost INT NOT NULL,
    reserved_seats INT NOT NULL,

    CONSTRAINT fk_users_username
    FOREIGN KEY (username)
    REFERENCES users (username)
    ON DELETE CASCADE
);

