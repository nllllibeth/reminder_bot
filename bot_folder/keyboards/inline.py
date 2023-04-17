from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_commands = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text= 'set',
            #url='/set',
            callback_data= 'command_set'
        ),
        InlineKeyboardButton(
            text= 'edit',
            #url='/set',
            callback_data= 'command_edit'
        ),
        InlineKeyboardButton(
            text= 'stop',
            callback_data= 'command_stop'
        )
    ]
])

inline_frequency = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text = 'once a day',
            callback_data='frequency_1'
        )
    ],
    [
        InlineKeyboardButton(
            text = 'twice a day',
            callback_data='frequency_2'
        )
    ],
    [
        InlineKeyboardButton(
            text = 'three times a day',
            callback_data='frequency_3'
        )
    ]
])

inline_answer = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text = 'yes', 
            callback_data="answer_yes"
        ), 
        InlineKeyboardButton(
            text= 'no',
            callback_data='answer_no'
        ),
    ]
])

def generate_delete_reminders_names(namelist):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for name in namelist:
        markup.add(InlineKeyboardButton(
            text=name[0],
            callback_data = name[0] + '_' + 'delete'
        ))
    return markup

def generate_edit_reminders_names(namelist):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for name in namelist:
        markup.add(InlineKeyboardButton(
            text=name[0],
            callback_data = name[0] + '_' + 'edit'
        ))
    return markup
