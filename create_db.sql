PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS sportsman;
CREATE TABLE sportsman
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    firstname VARCHAR(32),
    lastname  VARCHAR(32)
);
DROP TABLE IF EXISTS category;
CREATE TABLE category
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name      VARCHAR(32)
--     sportsman INTEGER,
--     FOREIGN KEY (sportsman) REFERENCES sportsman (id)

);
DROP TABLE IF EXISTS groups;
CREATE TABLE groups
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name      VARCHAR(32)
--     sportsman INTEGER,
--     category  INTEGER,
--     FOREIGN KEY (sportsman) REFERENCES sportsman (id),
--     FOREIGN KEY (category) REFERENCES category (id)
);



COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
