import logging
from aiogram.types import Message
from ..keyboards.inline import inline_commands, generate_edit_reminders_names, generate_delete_reminders_names
from ..fsm import StepsForm

async def send_welcome_message(message: Message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    logging.info(f'{user_id} {user_first_name}')
    await message.reply(f'Hi, {user_first_name}!\n\r\nPlease select a command:\n\r\n' \
        f'/set - to set pill reminder\r\n/stop - to stop reminder\r\n/edit - to edit existing reminder', 
        reply_markup=inline_commands)

async def get_form(message: Message):  # message_handler for /set command
    await message.answer(f'{message.from_user.first_name},\r\nPlease enter a name for your reminder')
    await StepsForm.GET_NAME.set() 

async def on_stop_command(message : Message, db_obs):  # message_handler for /stop command
    user_id = message.from_user.id
    namelist = db_obs.make_namelist(user_id)
    await message.answer('Please select the reminder that you want to stop')
    await message.answer("Reminders: ", reply_markup=generate_delete_reminders_names(namelist))

async def on_edit_command(message : Message, db_obs):  # message_handler for /edit command
    user_id = message.from_user.id
    namelist = db_obs.make_namelist(user_id)
    await message.answer('Please select the reminder that you want to edit')
    await message.answer("Reminders: ", reply_markup=generate_edit_reminders_names(namelist))
