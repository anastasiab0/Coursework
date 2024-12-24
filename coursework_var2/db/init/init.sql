-- Создание базы данных, если она отсутствует
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'coursework') THEN
        CREATE DATABASE coursework;
    END IF;
END $$;

-- Подключение к базе данных
\connect coursework;

-- Создание таблицы planes
CREATE TABLE IF NOT EXISTS planes (
    flight_num_planes TEXT PRIMARY KEY,
    type_la TEXT,
    bort_num TEXT
);

-- Создание таблицы flights
CREATE TABLE IF NOT EXISTS flights (
    flight_num TEXT PRIMARY KEY,
    city_1 TEXT,
    city_2 TEXT
);