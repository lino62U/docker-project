CREATE DATABASE IF NOT EXISTS myapp_db;

USE myapp_db;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  password VARCHAR(100)
);

INSERT INTO users (name, email, password)
VALUES
  ('Alice', 'alice@example.com', '1234'),
  ('Bob', 'bob@example.com', '5678');

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(100) NOT NULL,
    lastName VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    date DATE NOT NULL
);

INSERT INTO employees (id, firstName, lastName, email, salary, date)
VALUES
    (1, 'Susan', 'Jordon', 'susan@example.com', 95000.00, '2019-04-11'),
    (2, 'Adrienne', 'Doak', 'adrienne@example.com', 80000.00, '2019-04-17'),
    (3, 'Rolf', 'Hegdal', 'rolf@example.com', 79000.00, '2019-05-01'),
    (4, 'Kent', 'Rosner', 'kent@example.com', 56000.00, '2019-05-03'),
    (5, 'Arsenio', 'Grant', 'arsenio@example.com', 65000.00, '2019-06-13'),
    (6, 'Laurena', 'Lurie', 'laurena@example.com', 120000.00, '2019-07-30'),
    (7, 'George', 'Tallman', 'george@example.com', 90000.00, '2019-08-15'),
    (8, 'Jesica', 'Watlington', 'jesica@example.com', 60000.00, '2019-10-10'),
    (9, 'Matthew', 'Warren', 'matthew@example.com', 71000.00, '2019-10-15'),
    (10, 'Lyndsey', 'Follette', 'lyndsey@example.com', 110000.00, '2020-01-15');