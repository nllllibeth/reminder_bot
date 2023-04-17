import logging
import re
import sqlite3
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .states import StepsForm
from ..keyboards.inline import inline_frequency, inline_answer
from ..keyboards.reply import get_loc
from ..validation import *
from observer_pattern.subject.event import Event

storage = MemoryStorage()

async def start_form(call: CallbackQuery):
    await call.message.answer(f"{call.from_user.first_name}, \r\nPlease enter a name for your reminder.")
    await call.answer()
    await StepsForm.GET_NAME.set()

async def get_reminder_name(message: Message, state: FSMContext):
    reminder_name = message.text
    name_is_one_word = check_is_one_word(reminder_name)
    if name_is_one_word == True:
        async with state.proxy() as data:
            data['user_id'] = message.from_user.id
            data['reminder_name'] = reminder_name
        await message.answer(f"Success!\n\r\nNow please enter a message that you want to receive in the notifications")
        await StepsForm.GET_MSG.set()
    else:
        await message.answer("Please send one word for the name")


async def get_message(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['msg'] = message.text
    await message.answer(f'Good!\n\r\nNow please choose frequency for notifications',
                         reply_markup=inline_frequency)
    await StepsForm.GET_FREQUENCY.set()

async def get_frequency(callback: CallbackQuery, state: FSMContext):
    frequency_number = callback.data.split('_')[1]
    async with state.proxy() as data:
        data['frequency'] = frequency_number
        await callback.message.answer(f"Frequency {frequency_number} set succesfully!")
        await callback.message.answer("Now let's set time for your reminder.\
                                  \n\r\nTo begin with, set your time zone. Please share your location", reply_markup=get_loc)
        await callback.answer()
        await StepsForm.GET_TZ.set()

async def get_tz(message : Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude
    defined_location = get_location(latitude, longitude)
    country = defined_location[0]
    country_utc_offset = defined_location[1]
    country_utc_time = defined_location[2]
    async with state.proxy() as data:
        data['utc'] = country_utc_offset
    await message.answer("Location is set succesfully", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"Is {country_utc_time}, {country} {country_utc_offset} your time zone?", 
                         reply_markup=inline_answer)
    await StepsForm.GET_TIME.set()

async def get_time(callback: CallbackQuery, state: FSMContext):
    is_tz_correct = callback.data
    if is_tz_correct == 'answer_yes':
        await callback.answer()
        async with state.proxy() as data:
            if data['frequency'] == '3':
                await callback.message.answer("Now please enter 1st, 2nd, and 3rd time for your reminder in one line (in 24-hours format)") 
            elif data['frequency'] == '2':
                await callback.message.answer("Now please enter 1st and 2nd time for your reminder in one line (in 24-hours format)")
            else:
                await callback.message.answer("Now please enter time for your reminder in one line (in 24-hours format)")
        await StepsForm.FINISH.set()
    elif is_tz_correct == 'answer_no':
        await state.finish()
        await callback.message.answer("Please press /help command")
    await callback.answer()

async def finish(message: Message, state: FSMContext, controller): 
    time_str = message.text
    time_str = ''.join(time_str)
    time_splitted = re.split("[\s,;/.:]+", time_str)
    times = []
    incorrect_time_message = 'Entered time is incorrect.\
                                     \nPlease type times in one line with a comma\
                                     \nExample: 12:30, 00:30, 07:30'
    is_hours_minutes_correct = check_time_correctness(time_splitted)
    if is_hours_minutes_correct == False:
        await message.answer(incorrect_time_message)
    times = separate_times(time_splitted)
    if len(times) == 0:
        await message.answer(incorrect_time_message)
    for i in range(len(times)):
        current = datetime.strptime(times[i], "%H:%M")
        times[i] = datetime.strftime(current, "%H:%M")
    async with state.proxy() as data:
        data['time'] = times
    await message.answer(f"Setted time is {time_str}")

    try:
        async with state.proxy() as data:
            event = Event.build_event_to_create(
                data['user_id'], data['reminder_name'], data['msg'], 
                data['frequency'], data['utc'], data['time'])
        controller.receive_event(event)
    except sqlite3.IntegrityError:
        await message.answer("Sorry, reminder name should be unique\nPlease set reminder again /start")
        logging.error("sqlite3.IntegrityError")
    except Exception as e:
        await message.answer("Sorry, something went wrong\nPlease set reminder again /start")
        logging.error(f"Error in form.finish func {e}")
    else:
         await message.answer(f"Your reminder was set succesfully:\
                        \n\nName - {data['reminder_name']}\
                         \nMessage - {data['msg']}\
                         \nFrequency - {data['frequency']}  time(s) a day\
                         \nTime -  {time_str}")
    finally:
        await state.finish()
