DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `things`;

CREATE TABLE users (
    `id`       INTEGER PRIMARY KEY AUTOINCREMENT,
    `name`     TEXT UNIQUE NOT NULL,
    `username` TEXT UNIQUE NOT NULL,
    `hash`     TEXT UNIQUE NOT NULL
);

CREATE TABLE things (
    `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
    `name`  TEXT NOT NULL,
    `image` TEXT NOT NULL,
    `owner` INTEGER NOT NULL,
    FOREIGN KEY (`owner`) REFERENCES `users` (`id`)
);

