import sqlite3 as sq
from ...subject.event import Event

""" Class that defines time_records table in the reminders.db database"""
class Time_records_db(): 
    def __init__(self) -> None:
        self.db = sq.connect('reminders.db')
        self.cur = self.db.cursor()
    
    def fill_in_time(self, times : list, rem_id: int, event: Event) -> None:
        for time in times:
            hours = time.split(':')[0]
            minutes = time.split(':')[1]
            self.cur.execute(""" INSERT INTO time_records(hour, minutes, rem_id) VALUES(?, ?, ?)""", [hours, minutes, rem_id])
            event.time_id = self.cur.lastrowid
            self.db.commit() 
            
    def make_timelist(self, hour : str) -> list:
        raw_data = self.cur.execute(""" SELECT hour, minutes, user_id, msg, rem_id, time_id FROM time_records natural join reminders WHERE hour == ? ORDER BY hour ASC""", [hour]).fetchall() 
        timelist = []
        for line in raw_data: 
            if len(line) > 0:
                new_line = []
                for i in line:
                    new_line.append(i)
                timelist.append(new_line)
        return timelist
