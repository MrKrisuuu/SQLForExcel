-- people table
CREATE TABLE people (
    name,
    year,
    city
)

INSERT INTO people VALUES
    ("Krzysztof", 2000, "Krakow"),
    ("Jakub", 1999, "Skawina"),
    ("Ewa", 2000, "Niegardow"),
    ("Pawel", 2000, "Krakow"),
    ("Damian", 1996, "Krakow")

-- colors table
CREATE TABLE colors (
    name,
    points
)

INSERT INTO colors VALUES
    ("red", 1),
    ("green", 3),
    ("blue", 5),
    ("white"  ,2),
    ("black", 4)


-- likes table
CREATE TABLE likes (
    id_person,
    id_color
)

INSERT INTO likes VALUES
    (1, 3),
    (1, 1),
    (5, 4),
    (2, 1),
    (2, 5),
    (3, 1),
    (3, 2),
    (5, 2),
    (3, 3),
    (4, 2),
    (5, 1)

UPDATE likes l
SET l.id_color = 5
WHERE l.id == 2

DELETE FROM likes l
WHERE l.id_person == 5

