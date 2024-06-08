from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import keyboards.keyboards as kb

from DB.models import Session, User
from DB.procedure import check_exist_phone

reg_router = Router()

class Reg(StatesGroup):
    phone_number = State()
    api_id = State()
    api_hash = State()


@reg_router.message(Command('register'))
async def reg_name(messgae: Message, state: FSMContext):
    await state.set_state(Reg.phone_number)
    await messgae.answer("Share own phone number", reply_markup=kb.markup_request_phone)
    

@reg_router.message(Reg.phone_number)
async def reg_api_id(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    exist_phone = check_exist_phone(phone)

    if exist_phone:
        await message.answer('You have already registered', reply_markup=ReplyKeyboardRemove())
        
    else:
        await state.update_data(phone_info=message.contact)
        await state.set_state(Reg.api_id)
        await message.answer('Enter you api_id:', reply_markup=ReplyKeyboardRemove())


@reg_router.message(Reg.api_id)
async def reg_api_id(message: Message, state: FSMContext):
    await state.update_data(api_id=message.text)
    await state.set_state(Reg.api_hash)
    await message.answer('Enter you api_hash:')


@reg_router.message(Reg.api_hash)
async def reg_api_id(message: Message, state: FSMContext):
    await state.update_data(api_hash=message.text)
    with Session.begin() as session:
        data = await state.get_data()
        user = User(name=data['phone_info'].first_name, 
                    phone_number=data['phone_info'].phone_number,
                    api_id=data['api_id'], 
                    api_hash=data['api_hash'], 
                    user_id=data['phone_info'].user_id)
        state.clear()
        session.add(user)
        session.commit()
    await message.answer('Successfully registered!')
