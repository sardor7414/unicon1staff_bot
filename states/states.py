from aiogram.dispatcher.filters.state import StatesGroup, State


class AppealState(StatesGroup):
    region_id = State()
    district_id = State()
    member_id = State()
    organization = State()
    task_id = State()
    location = State()
    image = State()


