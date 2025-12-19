DROP TABLE IF EXISTS exhibition CASCADE;
DROP TABLE IF EXISTS review CASCADE;
DROP TABLE IF EXISTS rating_desc CASCADE;
DROP TABLE IF EXISTS incident CASCADE;
DROP TABLE IF EXISTS incident_type CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS floor_assignment CASCADE;
DROP TABLE IF EXISTS floor CASCADE;

CREATE TABLE department(
    department_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE NOT NULL
);
CREATE TABLE exhibition(
    exhibition_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_code VARCHAR(20) UNIQUE NOT NULL,
    exhibition_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    description TEXT
);
CREATE TABLE rating_desc(
    rating_id SMALLINT PRIMARY KEY,
    description VARCHAR(50) NOT NULL
);
CREATE TABLE review(
    review_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_id INT NOT NULL,
    at TIMESTAMP NOT NULL CHECK (at <= CURRENT_TIMESTAMP),
    rating_id SMALLINT NOT NULL,
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id),
    FOREIGN KEY (rating_id) REFERENCES rating_desc(rating_id)
);
CREATE TABLE incident_type(
    incident_type_id SMALLINT PRIMARY KEY,
    description TEXT NOT NULL
);
CREATE TABLE incident(
    incident_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_id INT NOT NULL,
    at TIMESTAMP NOT NULL CHECK (at <= CURRENT_TIMESTAMP),
    incident_type_id SMALLINT NOT NULL,
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id),
    FOREIGN KEY (incident_type_id) REFERENCES incident_type(incident_type_id)
);
CREATE TABLE floor(
    floor_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    floor_name VARCHAR(50) UNIQUE NOT NULL
);
CREATE TABLE floor_assignment(
    floor_assignment_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_id INT NOT NULL,
    floor_id INT NOT NULL,
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id),
    FOREIGN KEY (floor_id) REFERENCES floor(floor_id)
);

DROP TABLE IF EXISTS staging_exhibition;
DROP TABLE IF EXISTS staging_kiosk;
