import logging
from datetime import datetime, timedelta
from ..db_observer.db_obs import DB_Observer
from observer_pattern.subject.controller import Controller
from .sender_obs import Sender

""" Class that creates Sender observer instances for current and next hours"""
class Timetable_maker():
    def __init__(self, db_obs: DB_Observer, current_time : datetime, controller: Controller, bot, scheduler):
        self.current_time = current_time  # datetime obj 
        self.timedelta = timedelta(hours=1) 
        self.db_obs = db_obs
        self.controller = controller
        self.bot = bot
        self.scheduler = scheduler
        self.__initialize_senders(self.current_time)

    def __initialize_senders(self, current_time : datetime):
        logging.info("Def initial_sender is running")
        timelist = self.db_obs.make_timelist(current_time)
        self.current_sender = Sender(self.current_time, timelist, self.bot, self.scheduler) 
        self.current_sender.subscribe(self.controller)
        self.current_sender.send_notification()
        next_time = current_time + self.timedelta
        
        timelist = self.db_obs.make_timelist(next_time)
        self.next_sender = Sender(next_time, timelist, self.bot, self.scheduler)
        self.next_sender.subscribe(self.controller)
        self.next_sender.send_notification()
        self.__scheduling()

    def __do_every_hour(self):
        self.current_sender = self.next_sender
        next_time = self.current_time + self.timedelta + self.timedelta
        timelist = self.db_obs.make_timelist(next_time)
        self.next_sender = Sender(next_time, timelist, self.bot, self.scheduler)
        self.next_sender.subscribe(self.controller) 
        self.next_sender.send_notification()
  
    def __scheduling(self):
        self.scheduler.add_job(self.__do_every_hour, trigger='interval', hours=1)
        logging.info("Def scheduling is running")
