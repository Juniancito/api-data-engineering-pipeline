-- 1. Consultar todos los usuarios
SELECT *
FROM users;

-- 2. Cantidad de usuarios por ciudad
SELECT
    city,
    COUNT(*) AS total_users
FROM users
GROUP BY city
ORDER BY total_users DESC;

-- 3. Empresas registradas
SELECT
    company,
    COUNT(*) AS total_users
FROM users
GROUP BY company
ORDER BY total_users DESC;

-- 4. Dominios de correo más utilizados
SELECT
    SPLIT_PART(email, '@', 2) AS email_domain,
    COUNT(*) AS total
FROM users
GROUP BY email_domain
ORDER BY total DESC;