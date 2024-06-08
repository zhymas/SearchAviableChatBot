from aiogram import html, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from DB.procedure import check_user
from aiogram.types import Message, ContentType

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


# @router.message(content_types=ContentType.DOCUMENT)
# async def handle_txt_file(message: Message):
#     document = message.document

#     if document.mime_type == 'text/plain' and document.file_name.endswith('.txt'):
#         user_id = message.from_user.id
#         await message.answer('Received a .txt file. Processing...')
        
#     else:
#         await message.answer('Please send a .txt file.')