import logging

class Event():
    event_id = 0

    def __init__(self, status: str, data: dict):
        self.event_id += 1
        self.status = status
        if status == "EventCreate":
            self.processCreate(data)
        elif status == "EventRequestEdit":
            self.processRequestEdit(data)
        elif status == 'EventReceiveEdit':
            self.processReceiveEdit(data)
        elif status == "NamesListRequest":
            self.processRequest(data)
        elif status == "EventDelete":
            self.processDelete(data)
        else: 
            logging.warning("Something went wrong with Event init")


    def processCreate(self, data: dict):
        self.id = data['user_id'] 
        self.name = data['reminder_name']
        self.msg = data['message']
        self.frequency = data['frequency']
        self.utc = data['utc']
        self.time = data['time']  
        logging.info(f"Event # {self.event_id} is sent to Controller")

    def processDelete(self, data: dict):
        self.name = data['reminder_name']
    
    def processRequestEdit(self, data: dict):
        self.id = data['user_id']
        self.old_name = data['reminder_name']
    
    def processReceiveEdit(self, data : dict):
        self.id = data['user_id']
        self.new_name = data['new_name']
        self.new_msg = data['new_msg']

    def processRequest(self, data: dict):
        self.id = data['user_id']
     