from enum import Enum

""" Class that enumerate all statuses of Event"""
class Event_status(Enum):
    EVENT_TO_CREATE = 1
    EVENT_TO_EDIT = 2
    EVENT_TO_DELETE = 3

    def __str__(self):
      return self.name

""" Class that displays data received from the Bot, and will be sent as update for all the Observers"""
class Event():
    cls_id = 1

    def __init__(self):
        self.event_id = Event.cls_id
        Event.cls_id += 1

    @staticmethod
    def build_event_to_delete(reminder_name : str):
        event = Event()
        event.status = Event_status.EVENT_TO_DELETE
        event.reminder_name = reminder_name
        return event
    
    @staticmethod
    def build_event_to_edit(user_id, new_reminder_name, new_msg):
        event = Event()
        event.user_id = user_id
        event.status = Event_status.EVENT_TO_EDIT
        event.new_reminder_name = new_reminder_name
        event.new_msg = new_msg
        event.rem_id = None
        event.frequency = None
        return event
    
    @staticmethod
    def build_event_to_create(user_id, reminder_name, msg, frequency, utc, time):
        event = Event()
        event.status = Event_status.EVENT_TO_CREATE
        event.user_id = user_id
        event.reminder_name = reminder_name
        event.msg = msg
        event.frequency = frequency
        event.utc = utc
        event.time = time 
        event.rem_id = None
        event.time_id = None
        return event
