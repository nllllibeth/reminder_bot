import logging
from aiogram.types import Message
from ..keyboards.inline import inline_commands, generate_edit_reminders_names, generate_delete_reminders_names
from ..fsm import StepsForm

async def send_welcome_message(message: Message):
    tg_user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    logging.info(f'{tg_user_id} {user_first_name}')
    await message.reply(f'Hi, {user_first_name}!\n\r\nPlease select a command:\n\r\n' \
        f'/set - to set pill reminder\r\n/stop - to stop reminder\r\n/edit - to edit existing reminder', 
        reply_markup=inline_commands)

async def get_form(message: Message):
    await message.answer(f'{message.from_user.first_name},\r\nPlease enter a name for your reminder')
    await StepsForm.GET_NAME.set() 

async def stop_command(message : Message, db_obs):
    user_id = message.from_user.id
    names_list = db_obs.getNamesList(user_id)
    await message.answer('Please select a reminder that you want to stop')
    await message.answer("Reminders: ", reply_markup=generate_delete_reminders_names(names_list))

async def edit_command(message : Message, db_obs):
    user_id = message.from_user.id
    names_list = db_obs.getNamesList(user_id)
    await message.answer('Please select a reminder that you want to edit')
    await message.answer("Reminders: ", reply_markup=generate_edit_reminders_names(names_list))
   