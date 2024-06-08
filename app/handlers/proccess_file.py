import asyncio
import re
from telethon import TelegramClient, errors
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.types import Channel, Chat
from aiogram.types import FSInputFile
import os
from aiogram.types import Message
import time

async def process_file(api_id, api_hash, phone_number, message: Message, bot, file_path):
    input_file = file_path
    output_file = f'accessible_chat_urls_user_id_{message.from_user.id}.txt'

    client = TelegramClient('session', api_id, api_hash)
    
    await client.connect()
    if not await client.is_user_authorized():
        return await message.answer('123')
    await message.answer("Client Created")

    accessible_chats = []

    with open(input_file, 'r') as file:
        groups = file.read().splitlines()

    for group in groups:
        time.sleep(5)
        try:
            await client(JoinChannelRequest(group))
            await message.answer(f"Joined group: {group}")

            entity = await client.get_entity(group)
            try:
                await client.send_message(entity, 'Test message')
                accessible_chats.append(group)
            except errors.ChatWriteForbiddenError:
                await message.answer(f"No write access to {group}")
                await client(LeaveChannelRequest(entity))
            except Exception as e:
                await message.answer(f"Error occurred while sending message to {group}: {e}")
                await client(LeaveChannelRequest(entity))
        except Exception as e:
            error_message = str(e)
            match = re.search(r"A wait of (\d+) seconds is required", error_message)
            if match:
                wait_seconds = int(match.group(1))
                await message.answer(f"Wait for {wait_seconds} seconds required")
                time.sleep(wait_seconds)
            else:
                await message.answer(f"Error joining group: {group}, skipping...")

    with open(output_file, 'w') as f:
        for chat in accessible_chats:
            f.write(chat + '\n')
            
    document = FSInputFile(path=output_file)
    await bot.send_document(message.chat.id, document)
    os.remove(output_file)
    os.remove(input_file)
    await client.disconnect()
