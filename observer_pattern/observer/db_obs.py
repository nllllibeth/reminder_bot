import sqlite3 as sq
import logging 
from .observer import Observer
from ..subject.controller import Controller
from ..subject.event import Event


class Reminders_db():
    def __init__(self):
        self.db = sq.connect('reminders.db')
        self.cur = self.db.cursor()
    
    def fill_in_reminders(self, event: Event):
        self.cur.execute(""" INSERT INTO reminders(user_id, name, msg, frequency, utc) VALUES(?, ?, ?, ?, ?)""", (event.id, event.name, event.msg, event.frequency, event.utc))
        self.db.commit() 
    
    def get_rem_id(self, name: str) -> int:
        rem_id = self.cur.execute(""" SELECT rem_id FROM reminders WHERE name = ? ORDER BY rem_id DESC LIMIT 1""", 
                                  [name]).fetchone()[0]
        self.db.commit()  #not necesessary
        return rem_id
    
    def get_names_list(self, user_id: int) -> list:
        raw_data = self.cur.execute(""" SELECT name FROM reminders WHERE user_id = ?""",
                                     [user_id]).fetchall()
        names_list = []
        for line in raw_data:
            if len(line) > 0:
                names_list.append(line)
        return names_list
    
    def delete_record(self, rem_id : int):
        try:
            self.cur.execute("PRAGMA foreign_keys=ON")
            self.cur.execute(""" DELETE from reminders WHERE rem_id = ?""",
                                 [rem_id])
            self.db.commit()
            logging.info(f"Record {rem_id} rem_id deleted succesfully")
        except sq.Error as error:   
            logging.error("Erorr occured with SQLite3", error)
        
    def edit_record(self, rem_id : int, new_name: str, new_msg : str):
        try: 
            self.cur.execute(""" UPDATE reminders 
                                    SET name = ?, 
                                        msg = ?
                                    WHERE rem_id = ?""",
                                    [new_name, new_msg, rem_id])
            self.db.commit()
            logging.info(f"Reminder {rem_id} was edited with new data {new_name}, {new_msg}")
        except sq.Error as error:   
            logging.error("Erorr occured with SQLite3", error)


class Time_records_db():
    def __init__(self) -> None:
        self.db = sq.connect('reminders.db')
        self.cur = self.db.cursor()
    
    def fill_in_time(self, event: Event, rem_id: int):
        for time in event.time:
            hour = time.split(':')[0]
            minutes = time.split(':')[1]
            self.cur.execute(""" INSERT INTO time_records(hour, minutes, rem_id) VALUES(?, ?, ?)""", [hour, minutes, rem_id])
            self.db.commit() 

    def make_timelist(self, hour : str):
        raw_data = self.cur.execute(""" SELECT hour, minutes, user_id, msg FROM time_records natural join reminders WHERE hour == ? ORDER BY hour ASC""", [hour]).fetchall() 
        timelist = []
        for line in raw_data: 
            if len(line) > 0:
                timelist.append(line)
        return timelist
    

class DB_Observer(Observer):
    def __init__(self, controller: Controller):
        self.__controller = controller
        self.event: Event = None
        self.reminders = Reminders_db()
        self.time_records = Time_records_db()
        self.reminders_to_edit = {}

    
    def update(self, event: Event): 
        logging.debug("DB_Observer received an update")

        if event.status == 'NamesListRequest':
            user_id = event.id
            list = self.getNamesList(user_id)
            return list 
        elif event.status == "EventDelete":
            name = event.name
            rem_id = self.reminders.get_rem_id(name)
            self.reminders.delete_record(rem_id)
        elif event.status == 'EventRequestEdit':
            user_id = event.id
            old_name = event.old_name
            rem_id = self.reminders.get_rem_id(old_name)
            data = []
            data.append(old_name)
            data.append(rem_id)
            self.reminders_to_edit[user_id] = data
            logging.debug("reminders to edit", self.reminders_to_edit)
        elif event.status == 'EventReceiveEdit':
            user_id = event.id 
            new_name = event.new_name
            new_msg = event.new_msg
            if user_id in self.reminders_to_edit:
                rem_id = self.reminders_to_edit[user_id][1]
                self.reminders.edit_record(rem_id, new_name, new_msg)
                logging.debug("Func edit record called")
        else:
            self.reminders.fill_in_reminders(event)
            name = event.name
            rem_id = self.reminders.get_rem_id(name) 
            self.time_records.fill_in_time(event, rem_id)
            self.reminders.get_names_list(event.id)
        logging.info("DB_observer processed an update")

    def subscription(self):
        self.__controller.attach(self)
        logging.info("DB_Observer subscribed to Controller updates")
    
    def request_timelist(self, hour : str):
        timelist = self.time_records.make_timelist(hour)
        return timelist

    def getNamesList(self, user_id):
        list = self.reminders.get_names_list(user_id)
        return list
    
        

    

    

        
        


        
        
        



    

