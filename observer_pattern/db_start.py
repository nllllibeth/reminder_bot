import sqlite3 as sq
import logging

def reminders_start() -> None:
    db = sq.connect('reminders.db')
    cur = db.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS reminders(
            rem_id      INTEGER NOT NULL PRIMARY KEY,
            user_id     TEXT NOT NULL,
            name        TEXT,
            msg         TEXT, 
            frequency   TEXT, 
            utc          TEXT,
            UNIQUE(user_id, name) )""")
    db.commit()

def time_records_start() -> None:
    db = sq.connect('reminders.db')
    cur = db.cursor()
    cur.execute("PRAGMA foreign_keys=ON")
    cur.execute("""CREATE TABLE IF NOT EXISTS time_records(
            time_id   INTEGER NOT NULL PRIMARY KEY,
            hour      TEXT, 
            minutes   TEXT,
            rem_id    INTEGER,
            FOREIGN KEY (rem_id) REFERENCES reminders (rem_id) ON DELETE CASCADE)""")
    db.commit()

def reminders_drop() -> None:
    db = sq.connect('reminders.db')
    cur = db.cursor()
    cur.execute("DROP TABLE reminders")
    db.commit()

def time_records_drop() -> None:
    db = sq.connect('reminders.db')
    cur = db.cursor()
    cur.execute("DROP TABLE reminders")
    db.commit()

""" Function for starting reminders.db databases 
    and creating reminders and time_records tables in it"""
def db_start() -> None:
    reminders_start()
    time_records_start()
    logging.info("Tables reminders and time_records created successfully")
