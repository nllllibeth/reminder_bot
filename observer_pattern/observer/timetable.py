import logging
from datetime import datetime, timedelta

from .db_obs import DB_Observer
from observer_pattern.subject.controller import Controller
from .sender_obs import Sender
 

class Timetable_maker():
    def __init__(self, db_obs: DB_Observer, current_time : datetime, controller: Controller, bot, scheduler):
        self.current_time = current_time #datetime obj 
        self.current_hour_str = datetime.strftime(self.current_time, '%H')  #str
        self.timedelta = timedelta(hours=1) 
        self.next_time = current_time + self.timedelta #datetime obj
        self.next_hour_str = datetime.strftime(self.next_time, '%H') #str


        self.db_obs = db_obs
        self.controller = controller
        self.bot = bot
        self.scheduler = scheduler
        self.initial_sender(self.current_hour_str, self.next_hour_str) #int int

    
    def initial_sender(self, current_hour_str : str, next_hour_str : str): #можно передать сразу сюда current и next hour
        logging.info("Def initial_sender is running")
        timelist = self.db_obs.request_timelist(current_hour_str)
        logging.debug(f"1st Timelist for current_hour {timelist}")
        self.current_sender = Sender(self.current_time, current_hour_str, timelist, self.bot, self.scheduler) 
        self.current_sender.subscription(self.controller)
        self.current_sender.sending_message()
        logging.debug(f"Next hour str for timelist {next_hour_str}")
        timelist = self.db_obs.request_timelist(next_hour_str)
        logging.debug(f"2nd Timelist for next_hour {timelist}")
        self.next_sender = Sender(self.next_time, next_hour_str, timelist, self.bot, self.scheduler)
        self.next_sender.subscription(self.controller)
        self.next_sender.sending_message()
    
        self.scheduling()

    def do_every_hour(self):
        self.current_sender = self.next_sender
        self.current_hour_str = self.next_hour_str #теперь текущий час = след часу
        self.next_time = self.next_time + self.timedelta
        self.next_hour_str = datetime.strftime(self.next_time, '%H')
        timelist = self.db_obs.request_timelist(hour=self.next_hour_str)
        self.next_sender = Sender(self.next_time, self.next_hour_str, timelist, self.bot, self.scheduler)
        self.next_sender.sending_message()
  

    def scheduling(self):
        self.scheduler.add_job(self.do_every_hour, trigger='interval', hours=1)
        logging.info("Def scheduling is running")
