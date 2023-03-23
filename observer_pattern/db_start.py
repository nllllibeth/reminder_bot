import sqlite3 as sq
import logging

class Reminders_start():
    def __init__(self):
        self.db = sq.connect('reminders.db')
        self.cur = self.db.cursor()
    
    def db_start(self):
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS reminders(
            rem_id      INTEGER NOT NULL PRIMARY KEY,
            user_id     TEXT NOT NULL,
            name        TEXT,
            msg         TEXT, 
            frequency   TEXT, 
            utc          TEXT,
            UNIQUE(user_id, name) 
    )
    """)
        self.db.commit()

    def drop_tables(self):
        self.cur.execute("DROP TABLE reminders")
        self.db.commit()

class Time_records_start():
    def __init__(self) -> None:
        self.db = sq.connect('reminders.db')
        self.cur = self.db.cursor()
    
    def db_start(self):
        self.cur.execute("PRAGMA foreign_keys=ON")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS time_records(
            time_id   INTEGER NOT NULL PRIMARY KEY,
            hour      TEXT, 
            minutes   TEXT,
            rem_id    INTEGER,
            FOREIGN KEY (rem_id) REFERENCES reminders (rem_id) ON DELETE CASCADE)""")
        self.db.commit()
    
    def drop_tables(self):
        self.cur.execute("DROP TABLE time_records")
        self.db.commit()

def db_start():

    reminders = Reminders_start()
    reminders.db_start()
    time_records = Time_records_start()
    time_records.db_start()
    logging.info("Tables reminders and time_records created successfully")

    """reminders.drop_tables()
    time_records.drop_tables()"""


    