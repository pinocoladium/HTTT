import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_bot import contents
from telegram_bot.integration import (add_to_whitelist, check_imei,
                                      check_user_in_whitelist)

TOKEN = os.getenv("BOT_TOKEN")

storage = MemoryStorage()
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)
router = Router(name=__name__)


class Form(StatesGroup):
    check_imei = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await bot.send_sticker(
        chat_id=message.chat.id,
        sticker=contents.GREETING_STICKER,
    )
    await message.answer("Привет, я бот, который сможет помочь тебе расшифровать IMEI")
    user_in_whitelist = await check_user_in_whitelist(message.from_user.id)
    if user_in_whitelist:
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="Проверить IMEI", callback_data="precheck_imei"
            )
        )
        await message.answer(
            "Мы уже с тобой знакомы, так что жми кнопку",
            reply_markup=builder.as_markup(),
        )
    elif user_in_whitelist is False:
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="Попасть в список", callback_data="get_there_white_list"
            )
        )
        await message.answer(
            "К сожалению, тебя еще нет в белом списке, жми кнопку",
            reply_markup=builder.as_markup(),
        )
    else:
        await message.answer("К сожалению, ты заблокирован(")
        await message.answer("Либо случились неполадки на линии")
        await message.answer("Необходимо обратиться в техподдержку")


@dp.callback_query(F.data == "get_there_white_list")
async def command_get_there_whitelist_handler(callback: types.CallbackQuery):
    user_added = await add_to_whitelist(
        callback.from_user.username, callback.from_user.id
    )
    if user_added:
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(
                text="Проверить IMEI", callback_data="precheck_imei"
            )
        )
        await bot.send_sticker(
            chat_id=callback.message.chat.id,
            sticker=contents.WHITELIST_STICKER,
        )
        await callback.message.answer(
            "Поздравляю!Ты успешно добавлен в белый список",
            reply_markup=builder.as_markup(),
        )
    else:
        await callback.answer("Что-то пошло не так(")
        await callback.answer("Необходимо обратиться в техподдержку")


@dp.callback_query(F.data == "precheck_imei")
async def command_check_imei_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Скинь IMEI, который необходимо проверить")
    await callback.message.answer(contents.TEXT_IMEI)
    await callback.message.answer("IMEI состоит из 15 арабских цифр")
    await state.set_state(Form.check_imei)


@dp.message(Command("check_imei"))
@dp.message(Form.check_imei)
async def command_check_imei(message: Message, state: FSMContext):
    if await check_user_in_whitelist(message.from_user.id):
        status, response = await check_imei(message.text)
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(text="ЖМИ", callback_data="precheck_imei")
        )
        if status == 200:
            await state.clear()
            await message.answer(
                "\n".join([f"{key}: {value}" for key, value in response.items()])
            )
            await message.answer(
                "Если захочешь запросить еще, то", reply_markup=builder.as_markup()
            )
        elif status == 400:
            await state.clear()
            await bot.send_sticker(
                chat_id=message.chat.id,
                sticker=contents.BAD_VALIDATION_STICKER,
            )
            await message.answer("IMEI не прошел валидацию(")
            await message.answer("\n".join(value[0] for value in response.values()))
            await message.answer(
                "Если захочешь запросить еще, то", reply_markup=builder.as_markup()
            )
        else:
            await message.answer(
                "Непридвиденная ситуация, попробуйте еще раз отправить IMEI"
            )
    else:
        await bot.send_sticker(
            chat_id=message.chat.id,
            sticker=contents.CRINGE_STICKER,
        )
        await message.answer("Возможно тебя нет в белом списке, жми команду - /start")


@dp.message()
@dp.message(Command("help"))
async def echo_handler(message: types.Message) -> None:
    await message.reply(
        "Я же не ChatGPT, реагировать на подобное внесюжетное обращение еще не умею ..."
    )
    await message.answer("Если необходимо начать заново - /start")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="ЖМИ", callback_data="precheck_imei"))
    await message.answer(
        "Если необходимо запросить IMEI", reply_markup=builder.as_markup()
    )


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
