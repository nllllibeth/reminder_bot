import logging 
from datetime import datetime
from ..observer import Observer
from ...subject.controller import Controller
from ...subject.event import Event, Event_status
from .reminders_db import Reminders_db
from .time_records_db import Time_records_db

""" Database observer that can create, edit, delete record based on received update,
    also it can retrieve data from the database for maintating outer functions and classes"""
class DB_Observer(Observer):
    def __init__(self, controller: Controller):
        self.__controller = controller
        self.event: Event = None
        self.reminders = Reminders_db()
        self.time_records = Time_records_db()
        self.reminders_to_edit = {}

    def update(self, event: Event):
        logging.debug("DB_Observer received an update")
        if event.status == Event_status.EVENT_TO_DELETE:
            self.__on_delete(event.reminder_name, event)
        elif event.status == Event_status.EVENT_TO_EDIT:
            self.__on_edit(event.user_id, event.new_reminder_name, event.new_msg, event)
        elif event.status == Event_status.EVENT_TO_CREATE:
            self.__on_create(event.user_id, event.reminder_name,
                           event.msg, event.frequency, 
                           event.utc, event.time, event)
        logging.info("DB_observer processed an update")

    def __on_delete(self, reminder_name, event): 
        rem_id = self.reminders.get_rem_id(reminder_name)
        event.rem_id = rem_id
        self.reminders.delete_record(rem_id)
        logging.info(f"Reminder # {rem_id} was deleted from DB")

    def __on_edit(self, user_id, new_name, new_msg, event):
        try:
            rem_id = self.reminders_to_edit[user_id]
            self.reminders.edit_record(rem_id, new_name, new_msg)
            event.rem_id = rem_id
            del self.reminders_to_edit[user_id]  
            logging.info(f"DB changes were made in reminder # {rem_id}")
        except KeyError:
            logging.error(f"KeyError : there're no reminders to edit from user {user_id}")

    def __on_create(self, user_id, reminder_name, msg, frequency, utc, time, event): 
        self.reminders.fill_in_reminders(user_id, reminder_name, msg, frequency, utc) 
        rem_id = self.reminders.get_rem_id(reminder_name) 
        event.rem_id = rem_id
        self.time_records.fill_in_time(time, rem_id, event)       
        logging.info("DB_observer processed an update")

    def subscribe(self):
        self.__controller.attach(self)
        logging.info("DB_Observer subscribed to Controller updates")
    
    def make_timelist(self, time : datetime) -> list: 
        hour_str = datetime.strftime(time, '%H')
        return self.time_records.make_timelist(hour_str)

    def make_namelist(self, user_id) -> list: 
        return self.reminders.get_names_list(user_id)
    
    def add_reminder_to_edit(self, user_id, previous_reminder_name) -> None:
        self.reminders_to_edit[user_id] = self.reminders.get_rem_id(previous_reminder_name)
