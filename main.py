import asyncio
import re

from aiofile import async_open
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command, Filter
from aiogram.methods import DeleteWebhook
from aiogram.types import *
from aiopath import AsyncPath
from deepgram import Deepgram

from config import *
from constants import *

bot = Bot(TOKEN)
dp = Dispatcher()

dg_client = Deepgram(DEEP_TOKEN)
brain = False


class Admin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMIN.values()


class Manager(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in MANAGER.values()


class DrZi(Filter):
    async def __call__(self, message: Message) -> bool:
        normalize_message = re.sub(r'\W|_|ʼ', ' ', message.text.lower())
        return not set(normalize_message.split()).isdisjoint(DOCTOR)


@dp.message(CommandStart())
async def starting(message: Message):
    await message.answer(START, 'MarkdownV2')


@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer(HELP, 'MarkdownV2', reply_markup=KB_HELP)


@dp.callback_query(F.data == 'Переклад')
async def help_translate(callback: CallbackQuery):
    await callback.message.answer(INSTRUCTION_TRANSLATE, 'MarkdownV2')


@dp.callback_query(F.data == 'Голосове')
async def help_voice(callback: CallbackQuery):
    await callback.message.answer(INSTRUCTION_VOICE, 'MarkdownV2')


@dp.message(Command('translate'))
async def translate_text(message: Message, choose_message: int = 1):
    if message.reply_to_message:
        await message.reply(f'Українською це:\n{await translit(message.reply_to_message.text)}')
    else:
        await bot.send_message(message.chat.id, THIS_MESSAGE,
                               reply_to_message_id=message.message_id - choose_message, reply_markup=KB_TEXT)


@dp.callback_query(F.data == 'text')
async def get_text(callback: CallbackQuery):
    await callback.message.edit_text(f'Українською це:\n{await translit(callback.message.reply_to_message.text)}')


@dp.message(Command('voice'))
async def translate_voice(message: Message, choose_message: int = 1):
    if message.reply_to_message:
        document = message.reply_to_message.voice
        await bot.download(document, f'voices/{document.file_id}.ogg')
        voice = await speech_to_text(document)
        await message.reply(f'Тут сказано:\n{voice}') if voice else VOICE_404
        await AsyncPath(f'voices/{document.file_id}.ogg').unlink()
    else:
        await bot.send_message(message.chat.id, THIS_AUDIO,
                               reply_to_message_id=message.message_id - choose_message, reply_markup=KB_AUDIO)


@dp.callback_query(F.data == 'speach')
async def get_voice(callback: CallbackQuery):
    document = callback.message.reply_to_message.voice
    await bot.download(document, f'voices/{document.file_id}.ogg')
    voice = await speech_to_text(document)
    await callback.message.edit_text(f'Тут сказано:\n{voice}') if voice else VOICE_404
    await AsyncPath(f'voices/{document.file_id}.ogg').unlink()


@dp.message(Command('id'), Admin())
async def get_id(message: Message):
    if message.reply_to_message and message.reply_to_message.contact:
        await message.reply(
            f"{message.reply_to_message.contact.first_name}'s ID: {message.reply_to_message.contact.user_id}."
        )
    elif message.reply_to_message:
        await message.reply(
            f"{message.reply_to_message.from_user.first_name}'s  ID: {message.reply_to_message.from_user.id}."
        )
    else:
        await message.reply(
            f"Hello {message.from_user.first_name}! Your ID: {message.from_user.id}."
        )


@dp.message(Command('settings'), Admin())
async def settings(message: Message):
    await message.reply(f'Налаштування\n\nМова розпізнавання голосу: {LANGUAGES.get(DG_OPTIONS.get("language"))}.',
                        reply_markup=KB_SETTINGS)


@dp.message(DrZi())
async def doctor(message: Message):
    await message.answer('Доктор Зі, до вас звертаються.')


@dp.message()
async def forwarded(message: Message):
    if message.forward_from and (message.chat.id == message.from_user.id):
        if message.text:
            await translate_text(message, 0)
        elif message.voice:
            await translate_voice(message, 0)


async def translit(message: str) -> str:
    layout = LAYOUTS.get('QWERTY', 'QWERTY')
    return message.translate(layout)


async def speech_to_text(voice: Voice) -> str:
    async with async_open(f'voices/{voice.file_id}.ogg', 'rb') as audio:
        source = {'buffer': audio, 'mimetype': voice.mime_type}
        response = await dg_client.transcription.prerecorded(source, DG_OPTIONS)
        return (response.get('results', VOICE_404).get('channels', VOICE_404)[0]
                .get('alternatives', VOICE_404)[0].get('transcript', VOICE_404))


async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    if Admin():
        await bot.set_my_commands([BotCommand(command=command[0], description=command[1]) for command in ADM_COMMANDS])
    else:
        await bot.set_my_commands([BotCommand(command=command[0], description=command[1]) for command in USR_COMMANDS])
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())