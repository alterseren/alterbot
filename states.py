from aiogram.fsm.state import State, StatesGroup

class SupportState(StatesGroup):
    waiting_for_message = State()

class UploadFileState(StatesGroup):
    waiting_for_file = State()

class EditProfileState(StatesGroup):
    waiting_for_birth_date = State()
    waiting_for_birth_city = State()