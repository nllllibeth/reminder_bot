import os
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, executor
from aiogram.types import ContentType

from bot_folder.handlers import *
from bot_folder.fsm.form import *
from bot_folder.fsm.states import StepsForm, StepsEdit

from observer_pattern.subject.controller import Controller
from observer_pattern.observer.db_obs import DB_Observer
from observer_pattern.db_start import db_start
from observer_pattern.observer.timetable import Timetable_maker


from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()


def register_handlers(dp: Dispatcher, controller : Controller, db_obs : DB_Observer):
    dp.register_message_handler(send_welcome_message, commands=['start', 'help'])
    dp.register_callback_query_handler(start_form, text='command_set')
    dp.register_message_handler(get_form, commands=['set'])
    dp.register_message_handler(lambda message: stop_command(message, db_obs), commands=['stop'])
    dp.register_message_handler(lambda message: edit_command(message, db_obs), commands=['edit'])
    dp.register_callback_query_handler(lambda call: select_command(call, db_obs), text= ['command_stop', 'command_edit']) 
    dp.register_message_handler(get_reminder_name, state=StepsForm.GET_NAME)
    dp.register_message_handler(get_message, state=StepsForm.GET_MSG, content_types=[ContentType.TEXT])
    dp.register_callback_query_handler(get_frequency, state=StepsForm.GET_FREQUENCY, text= ['frequency_1', 'frequency_2', 'frequency_3'])
    dp.register_message_handler(get_tz, state=StepsForm.GET_TZ, content_types=[ContentType.LOCATION])
    dp.register_callback_query_handler(get_time, state= StepsForm.GET_TIME, text=['answer_yes', 'answer_no'])
    dp.register_message_handler(lambda message, state: finish(message, state, controller), state=StepsForm.FINISH, content_types=[ContentType.TEXT])
    dp.register_callback_query_handler(lambda call: change_reminder(call, controller))
    dp.register_message_handler(lambda message, state: edit_reminder(message, state, controller), state=StepsEdit.EDIT, content_types=[ContentType.TEXT])


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
    TOKEN = os.getenv('TOKEN_REMINDER')

    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot=bot, storage=storage)

    controller = Controller()
    db_start() 
    db_obs = DB_Observer(controller)
    db_obs.subscription()
    scheduler.start()
    current_time = datetime.now() 
    timetable = Timetable_maker(db_obs, current_time, controller, bot, scheduler)

    register_handlers(dp, controller, db_obs)

    executor.start_polling(dp, 
                           skip_updates=True)
    