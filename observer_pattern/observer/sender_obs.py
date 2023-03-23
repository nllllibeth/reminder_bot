import logging
from datetime import datetime

from .observer import Observer
from ..subject.controller import Controller
from ..subject.event import Event


class Sender(Observer):
    def __init__(self, time : datetime, hour_str : str, timeslist : list, bot, scheduler):
        self.time = time # current or next time
        self.hour_str = hour_str
        self.timeslist = timeslist # list of tuples
        self.bot = bot
        self.scheduler = scheduler

    def subscription(self, controller : Controller):
        controller.attach(self)
        logging.info("Sender_obs subscribed to Controller updates")

    async def update_job(self, user_id, text, bot):
        await bot.send_message(user_id, text)
        print(f"UPDATE JOB : Message {text} sent to {user_id}")


    def update(self, event : Event):
        logging.debug("Update func in Sender called")
        if event.status == "EventCreate": 
            for time in event.time:
                event_hour = time.split(':')[0] 
                if event_hour == self.hour_str:
                    date_now = datetime.strftime(self.time, "%d/%m/%Y")
                    new_datetime = date_now + " " + time 
                    event_time = datetime.strptime(new_datetime, "%d/%m/%Y %H:%M")
                    self.scheduler.add_job(self.update_job, trigger='date', run_date=event_time, args=(event.id, event.msg, self.bot))
        else:
            pass
            #("Другой тип ивента")
    

    async def job(self, user_id, text, bot):
        await bot.send_message(user_id, text)
        logging.info(f"JOB : Message {text} sent to {user_id}")

    def sending_message(self):
        logging.debug("Def sending message called")
        for line in self.timeslist:
            line_hour = line[0]
            line_minutes = line[1]
            line_id = line[2]
            line_msg = line[3]

            line_str = line_hour + ':' + line_minutes
            date_now = datetime.strftime(self.time, "%d/%m/%Y")
            new_datetime = date_now + " " + line_str 
            line_time = datetime.strptime(new_datetime, "%d/%m/%Y %H:%M")
            self.scheduler.add_job(self.job, trigger='date', run_date=line_time, args=(line_id, line_msg, self.bot))
