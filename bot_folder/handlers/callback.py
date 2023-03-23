import logging
from aiogram.types import CallbackQuery, Message
from ..keyboards.inline import generate_delete_reminders_names, generate_edit_reminders_names
from observer_pattern.subject.event import Event
from aiogram.dispatcher import FSMContext
from ..fsm.states import StepsEdit
from ..validation import get_two_strings

"""async def answer_callback(call: CallbackQuery):
    if call.data == 'answer_no':
        await call.answer("Please press /help command")
    await call.answer()"""

async def select_command(call: CallbackQuery, db_obs):
    user_id = call.from_user.id
    names_list = db_obs.getNamesList(user_id)
    if call.data == 'command_stop':
        await call.bot.send_message(user_id, 'Please select a reminder that you want to stop')
        await call.bot.send_message(user_id, "Reminders: ", reply_markup=generate_delete_reminders_names(names_list))
    else:
        await call.bot.send_message(user_id, 'Please select a reminder that you want to edit')
        await call.bot.send_message(user_id, "Reminders: ", reply_markup=generate_edit_reminders_names(names_list))
    await call.answer()


async def change_reminder(call : CallbackQuery, controller):
    user_id = call.from_user.id
    reminder_name = call.data.split('_')[0]
    command = call.data.split('_')[1]
    logging.debug(f"ReminderName and command and call data {reminder_name}, {command}, {call.data}")
    event_data = {}
    event_data['reminder_name'] = reminder_name
    if command == 'delete':
        event = Event(status="EventDelete", data=event_data)
        await call.bot.send_message(user_id, 'Your reminder was deleted')
        controller.receive_event(event)
    elif command == 'edit':
        event_data['user_id'] = user_id
        event = Event(status="EventRequestEdit", data = event_data)
        controller.receive_event(event)
        await call.bot.send_message(user_id, 'Please type in new data in format\n\nname, message with a comma\n\n(Notice: you cannot change frequency or time, for that please delete your previous reminder and set a new one)')
        await StepsEdit.EDIT.set()
    await call.answer()

async def edit_reminder(message: Message, state: FSMContext, controller):
    user_id = message.from_user.id
    new_data = get_two_strings(str(message.text))
    try: 
        len(new_data[0]) > 0 and len(new_data[0]) > 0 == True
    except Exception as e:
        logging.error(f"Error in edit_reminder func : {e}")
        await message.answer("Please type new name and message in format:\nname, message")
    else:
        new_name = new_data[0]
        new_message = new_data[1]
    event_data = {}
    event_data['user_id'] = user_id
    event_data['new_name'] = new_name
    event_data['new_msg'] = new_message
    event = Event(status="EventReceiveEdit", data=event_data)
    logging.info(f"EventReceiveEdit {event_data}")
    controller.receive_event(event)
    await state.finish()
    await message.answer("Your reminder was succesfully edited")
