DROP TABLE IF EXISTS contacts;

CREATE TABLE contacts (
    num_pressed INTEGER PRIMARY KEY AUTOINCREMENT,
    telephone TEXT NOT NULL,
    created_date DATE NOT NULL DEFAULT (DATE()),
    created_time TIME NOT NULL DEFAULT (TIME('now', 'localtime'))
);