SELECT p.name, COUNT(c.name), SUM(c.points)
FROM people p
LEFT JOIN likes l ON l.id_person == p.id
LEFT JOIN colors c ON c.id == l.id_color
GROUP BY p.name