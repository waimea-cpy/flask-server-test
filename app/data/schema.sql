DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `thing`;

CREATE TABLE user (
    `id`       INTEGER PRIMARY KEY AUTOINCREMENT,
    `name`     TEXT UNIQUE NOT NULL,
    `username` TEXT UNIQUE NOT NULL,
    `hash`     TEXT UNIQUE NOT NULL
);

CREATE TABLE thing (
    `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
    `name`  TEXT NOT NULL,
    `owner` INTEGER NOT NULL,
    FOREIGN KEY (`owner`) REFERENCES `user` (`id`)
);

