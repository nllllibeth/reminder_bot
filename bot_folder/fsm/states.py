from aiogram.dispatcher.filters.state import State, StatesGroup

class StepsForm(StatesGroup):
    GET_NAME = State()
    GET_MSG = State()
    GET_FREQUENCY = State()
    GET_TZ = State()
    GET_TIME = State()
    FINISH = State()

class StepsEdit(StatesGroup):
    EDIT = State()
