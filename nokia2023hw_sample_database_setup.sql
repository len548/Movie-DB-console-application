drop database if exists nokia2023hw;
create database nokia2023hw;
use nokia2023hw;
CREATE TABLE movies (
    movie_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    director_name VARCHAR(255) NOT NULL,
    release_year YEAR(4) NOT NULL,
    length_minutes INT NOT NULL,
    CONSTRAINT unique_movie UNIQUE (title, director_name)
);

CREATE TABLE people (
    person_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    birth_year YEAR(4) NOT NULL
);

CREATE TABLE movie_actors (
    movie_id INT,
    actor_id INT,
    PRIMARY KEY (movie_id, actor_id),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (actor_id) REFERENCES people(person_id)
);

-- Populate people table with directors and actors
INSERT INTO people (name, birth_year) VALUES
    ('Director1', '1980'),
    ('Director2', '1975'),
    ('Actor1', '1990'),
    ('Actor2', '1985'),
    ('Actor3', '1980');

-- Populate movies table
INSERT INTO movies (title, director_name, release_year, length_minutes) VALUES
    ('Movie1', 'Director1', '2020', 120),
    ('Movie1', 'Director2', '2020', 120),
    ('Movie2', 'Director1', '2022', 110),
    ('Movie3', 'Director3', '2021', 105);

-- Populate movie_actors table
INSERT INTO movie_actors (movie_id, actor_id) VALUES
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 5),
    (3, 4),
    (4, 3),
    (4, 5);

