DROP TABLE IF EXISTS card
DROP TABLE IF EXISTS deck

CREATE TABLE card(
    id INTEGER PRIMARY KEY,
    front TEXT,
    back TEXT,
    repetition INTEGER DEFAULT 0,
    easiness FLOAT DEFAULT 2.5,
    `interval` INTEGER DEFAULT 1,
    last_review DATE DEFAULT "1970-01-01",
    next_review DATE DEFAULT (DATE('now')),
    deck_name VARCHAR
);

CREATE TABLE deck(
    id INTEGER PRIMARY KEY,
    name VARCHAR UNIQUE
);

CREATE TABLE learning(
card_id INTEGER,
review_date DATE DEFAULT (DATE('now')),
score INTEGER
)