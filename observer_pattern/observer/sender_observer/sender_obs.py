import logging
from datetime import datetime
from ..observer import Observer
from ...subject.controller import Controller
from ...subject.event import Event, Event_status

class Sender(Observer):
    """ Sender Observer that sends notifications to user from received updates, 
    and regularly according to timeslist of specified hour"""
    def __init__(self, time : datetime, timeslist : list, bot, scheduler):
        self.time = time 
        self.hour_str = datetime.strftime(time, '%H')
        self.timeslist = timeslist # list of tuples
        self.bot = bot
        self.scheduler = scheduler

    def subscribe(self, controller : Controller) -> None:
        controller.attach(self)
        logging.info("Sender_obs subscribed to Controller updates")

    async def update_job(self, user_id, text, bot):
        """ Function that sends a message to user using aiogram bot"""
        await bot.send_message(user_id, text)
        logging.info(f"UPDATE JOB : Message {text} sent to {user_id}")

    def update(self, event : Event):
        logging.debug("Update func in Sender called")
        if event.status == Event_status.EVENT_TO_CREATE: 
            self.__add_jobs(event)
        elif event.status == Event_status.EVENT_TO_EDIT:
            self.__edit_jobs(event.rem_id, event.new_msg, event.user_id)
        elif event.status == Event_status.EVENT_TO_DELETE:
            self.__delete_jobs(event.rem_id)
 
    async def job(self, user_id, text, bot):
        """ Function that sends a message to user using aiogram bot
        separate update_job and job for send_notifications function"""
        await bot.send_message(user_id, text)
        logging.info(f"JOB : Message {text} sent to {user_id}")

    def send_notification(self):
        logging.debug("Def sending message called")
        for line in self.timeslist:
            line_hour = line[0]
            line_minutes = line[1]
            line_user_id = line[2]
            line_msg = line[3]
            line_rem_id = line[4] #int
            line_time_id = line[5] #int

            line_str = line_hour + ':' + line_minutes
            date_now = datetime.strftime(self.time, "%d/%m/%Y")
            new_datetime = date_now + " " + line_str 
            line_time = datetime.strptime(new_datetime, "%d/%m/%Y %H:%M")
            job_id = str(line_rem_id) + '_' + str(line_time_id)
            self.scheduler.add_job(self.job, id = job_id, trigger='date', run_date=line_time, args=(line_user_id, line_msg, self.bot))
    
    def __edit_jobs(self, rem_id, new_msg, user_id):
        jobs = self.scheduler.get_jobs()
        for job in jobs:
            if job.id.split('_')[0] == str(rem_id):
                self.scheduler.modify_job(job_id = job.id, args=(user_id, new_msg, self.bot))
        logging.info(f"Jobs for rem_id # {rem_id} were modified")
    
    def __delete_jobs(self, rem_id):
        jobs = self.scheduler.get_jobs()
        for job in jobs:
            if job.id.split('_')[0] == str(rem_id):
                job.remove()
        logging.info(f"Jobs for rem_id # {rem_id} were removed")

    def __add_jobs(self, event):
        cnt = 0
        for time in event.time:
            cnt += 1
            event_hour = time.split(':')[0] 
            if event_hour == self.hour_str:
                date_now = datetime.strftime(self.time, "%d/%m/%Y")
                new_datetime = date_now + " " + time 
                event_time = datetime.strptime(new_datetime, "%d/%m/%Y %H:%M")
                job_id = str(event.rem_id) + "_" + str(cnt)
                self.scheduler.add_job(self.update_job, id = job_id, trigger='date', run_date=event_time, args=(event.user_id, event.msg, self.bot))
