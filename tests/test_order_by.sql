SELECT p.name, SUM(c.points), COUNT(c.id)
FROM people p
LEFT JOIN likes l ON l.id_person == p.id
LEFT JOIN colors c ON c.id == l.id_color
GROUP BY p.name
ORDER BY SUM(c.points), COUNT(c.id)