CREATE TABLE IF NOT EXISTS blackmail(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner INTEGER NOT NULL,
    message TEXT NOT NULL,
    said_by_user INTEGER NOT NULL
)