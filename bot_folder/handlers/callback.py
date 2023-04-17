import logging
from aiogram.types import CallbackQuery, Message
from ..keyboards.inline import generate_delete_reminders_names, generate_edit_reminders_names
from observer_pattern.subject.event import Event
from aiogram.dispatcher import FSMContext
from ..fsm.states import StepsEdit
from ..validation import get_two_strings

async def select_command(call: CallbackQuery, db_obs):
    user_id = call.from_user.id
    namelist = db_obs.make_namelist(user_id)
    if call.data == 'command_stop':
        await call.bot.send_message(user_id, 'Please select the reminder that you want to stop')
        await call.bot.send_message(user_id, "Reminders: ", reply_markup=generate_delete_reminders_names(namelist))
    else:
        await call.bot.send_message(user_id, 'Please select the reminder that you want to edit')
        await call.bot.send_message(user_id, "Reminders: ", reply_markup=generate_edit_reminders_names(namelist))
    await call.answer()

async def change_reminder(call : CallbackQuery, controller, db_obs):
    user_id = call.from_user.id
    reminder_name = call.data.split('_')[0]
    command = call.data.split('_')[1]
    if command == 'delete':
        event = Event.build_event_to_delete(reminder_name)
        controller.receive_event(event)
        await call.bot.send_message(user_id, 'Your reminder was deleted')
    elif command == 'edit':
        db_obs.add_reminder_to_edit(user_id, reminder_name)
        await call.bot.send_message(user_id, 'Please type in new data in format\n\nname, message with a comma\n\n(Notice: you cannot change frequency or time, for that please delete your previous reminder and set a new one)')
        await StepsEdit.EDIT.set()
    await call.answer()

async def edit_reminder(message: Message, state: FSMContext, controller):
    user_id = message.from_user.id
    new_data = get_two_strings(str(message.text))
    try: 
        len(new_data[0]) > 0 and len(new_data[1]) > 0 == True
    except Exception as e:
        logging.error(f"Error in edit_reminder func : {e}")
        await message.answer("Please type new name and message in format:\nname, message")
    else:
        new_reminder_name = new_data[0]
        new_msg = new_data[1]
        event = Event.build_event_to_edit(user_id, new_reminder_name, new_msg)
        controller.receive_event(event)
        await state.finish()
        await message.answer("Your reminder was succesfully edited")
