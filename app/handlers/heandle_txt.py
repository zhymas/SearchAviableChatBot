from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import html, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from DB.procedure import check_user
from .proccess_file import process_file

from telethon import TelegramClient, errors

txt_router = Router()

class Txt(StatesGroup):
    file = State()
    code = State()


@txt_router.message(Command('process_txt'))
async def process_txt(message: Message, state: FSMContext):
    await state.set_state(Txt.file)
    await message.answer("Please send the .txt file")


@txt_router.message(Txt.file)
async def process_txt_file(message: Message, state: FSMContext):
    document = message.document

    if document.mime_type == 'text/plain' and document.file_name.endswith('.txt'):
        bot = message.bot

        file = await bot.download(document)
        file_path = f'files/new_file_user_id_{message.from_user.id}.txt'
        with open(file_path, 'w', encoding='utf-8') as new_file:
            file.seek(0)
            new_file.write(file.read().decode('utf-8'))
            
        client = TelegramClient('session', '22250327', '576b8c9f2bc394d9d30be44ff1ff18b4')
        await client.connect()
        
        if not await client.is_user_authorized():
            sent_code = await client.send_code_request('+380994351331')
            await state.update_data(phone_hash=sent_code.phone_code_hash)
            await state.set_state(Txt.code)
            await message.answer('Enter the code from telegram:')
            
        else:
            await state.clear()
            return await process_file('22250327', '576b8c9f2bc394d9d30be44ff1ff18b4', '+380994351331', message, bot, file_path)
    else:
        await message.answer("Please send a valid .txt file")


@txt_router.message(Txt.code)
async def auth_user(message: Message, state: FSMContext):
    code = message.text
    print(code)
    client = TelegramClient('session', '22250327', '576b8c9f2bc394d9d30be44ff1ff18b4')
    await client.connect()
    data = await state.get_data()
    await client.sign_in(phone='+380994351331', code=code, phone_code_hash=data['phone_hash'])
    await message.answer('Created connect')