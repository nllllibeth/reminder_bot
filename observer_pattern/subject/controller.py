import logging
from .subject import Subject, Event

""" Class that receive an Event from the bot and notify about such an update all its Observers"""
class Controller(Subject):
    def __init__(self) -> None:
        super().__init__()
        self.events = [] 
    
    def receive_event(self, event: Event):
        logging.info(f"Controller accepted {event.status} #{event.event_id}")
        self.events.append(event)
        self.send_event(event)
    
    def remove_event(self, event: Event):
        self.events.remove(event)
        logging.info(f"Controller removed Event #{event.event_id} from the list of Events")
    
    def send_event(self, event: Event):
        if self.events:
            event = self.events[-1]
            self.notify(event)
            logging.info(f"Controller sent Event #{event.event_id} to Observers")
            self.remove_event(event)
        else:
            logging.info(f"There are no Events to work on")
