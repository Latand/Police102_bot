from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    FullName = State()
    Address = State()
    Geolocation = State()
    Description = State()
    Photo = State()
    UrgentStatus = State()
    Comment = State()
