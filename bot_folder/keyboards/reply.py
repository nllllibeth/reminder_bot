from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_loc = ReplyKeyboardMarkup(keyboard= [
    [
        KeyboardButton(
            text= 'loc',
            request_location=True,
        )
    ]
], resize_keyboard=True, one_time_keyboard=True)
