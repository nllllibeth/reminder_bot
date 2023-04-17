import sqlite3 as sq
import logging

""" Class that defines reminders table in the reminders.db database"""
class Reminders_db():
    def __init__(self):
        self.db = sq.connect('reminders.db')
        self.cur = self.db.cursor()
    
    def fill_in_reminders(self, user_id, reminder_name, msg, frequency, utc) -> None:
        self.cur.execute(""" INSERT INTO reminders(user_id, name, msg, frequency, utc) VALUES(?, ?, ?, ?, ?)""", (user_id, reminder_name, msg, frequency, utc))
        self.db.commit() 
    
    def get_rem_id(self, name: str) -> int:
        rem_id = self.cur.execute(""" SELECT rem_id FROM reminders WHERE name = ? ORDER BY rem_id DESC LIMIT 1""", 
                                  [name]).fetchone()[0]
        return rem_id
    
    def get_names_list(self, user_id: int) -> list:
        raw_data = self.cur.execute(""" SELECT name FROM reminders WHERE user_id = ?""",
                                     [user_id]).fetchall()
        names_list = []
        for line in raw_data:
            if len(line) > 0:
                names_list.append(line)
        return names_list
    
    def delete_record(self, rem_id : int) -> None:
        try:
            self.cur.execute("PRAGMA foreign_keys=ON")
            self.cur.execute(""" DELETE from reminders WHERE rem_id = ?""",
                                 [rem_id])
            self.db.commit()
            logging.info(f"Reminder {rem_id} was deleted succesfully")
        except sq.Error as error:   
            logging.error("Erorr occured with SQLite3 Reminders.delete_record", error)
        
    def edit_record(self, rem_id : int, new_name: str, new_msg : str) -> None:
        try: 
            self.cur.execute(""" UPDATE reminders 
                                    SET name = ?, 
                                        msg = ?
                                    WHERE rem_id = ?""",
                                    [new_name, new_msg, rem_id])
            self.db.commit()
            logging.info(f"Reminder {rem_id} was edited with new data {new_name}, {new_msg}")
        except sq.Error as error:   
            logging.error("Erorr occured with SQLite3 in Reminders.edit_record", error)
