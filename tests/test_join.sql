SELECT p.name, c.name
FROM people p
JOIN likes l ON l.id_person == p.id
JOIN colors c ON c.id == l.id_color