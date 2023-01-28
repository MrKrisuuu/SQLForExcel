--SELECT p.name, COUNT(c.name), SUM(c.points)
--FROM people p
--LEFT JOIN likes l ON l.person == p.id
--LEFT JOIN colors c ON c.id == l.color
--GROUP BY p.name

--SELECT p.name, c.name, c.points
--FROM people p
--LEFT JOIN likes l ON l.person == p.id
--LEFT JOIN colors c ON c.id == l.color

SELECT p.name, AVG(c.points)
FROM people p
LEFT JOIN likes l ON l.id_person == p.id
LEFT JOIN colors c ON c.id == l.id_color
GROUP BY p.name

--DELETE FROM people p
--WHERE p.year == 2000

--SELECT *
--FROM people

