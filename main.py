from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData


from config import TOKEN, TIME_DELTA

from localisation_ru import localisation

import logging, random, math, re

from function import Function
function = Function()

from session import SessionHelper
session = SessionHelper()

bot = Bot(token=TOKEN)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    me = await bot.get_me()
    await message.reply(f"{localisation['start1']} /game@{me.username} {localisation['start2']}")

game = CallbackData("game", "action")

def keyboard_add():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text=localisation['see_word'], callback_data=game.new(action="see_word")),
        types.InlineKeyboardButton(text=localisation['next_word'], callback_data=game.new(action="next_word"))
    ]
    keyboard.add(*buttons)
    return keyboard

#Info
@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    with open("info.json", "r") as file:
        lines =file.readlines()
        text = ''
        for line in lines:
            text += line
        await message.reply(text, disable_web_page_preview=True)

@dp.message_handler(commands=['game'])
async def game_start(message: types.Message):
    data = session.read_data()
    if(data['id_chat'] == message.chat.id):
        if(data['id_user'] == 0 or not function.time_checker(data['time']) or data['word'] == ''):
            function.update_user(message.from_user.id, data['id_chat'])  
            await message.answer(f"<a href='{message.from_user.url}'>{message.from_user.first_name}</a> {localisation['describe_word']}", reply_markup=keyboard_add(), parse_mode=types.ParseMode.HTML)
        else: 
            await message.reply(f"{localisation['gamestart_1']} {str(math.ceil((TIME_DELTA - function.delta_time(data['time']))/60))} {localisation['gamestart_2']}")
    else:
        await message.reply(localisation['notchat'])

@dp.message_handler(commands=['rating'])
async def rating(message: types.Message):
    data = session.read_data()
    if(data['id_chat'] == message.chat.id):
        try:
            await message.reply(f"<b>{localisation['top']}</b> 🦔 \n\n{function.get_top()}", parse_mode=types.ParseMode.HTML)    
        except KeyError:
            await message.reply(f"{localisation['error']} \n {KeyError}", parse_mode=types.ParseMode.HTML)
    else:
        await message.reply(localisation['notchat'])


@dp.callback_query_handler(game.filter(action=["see_word"]))
async def see_word(call: types.CallbackQuery):
    data = session.read_data()
    if(call.from_user.id == data['id_user']):
        await call.answer(data['word'], show_alert=True)
    else:
        await call.answer(localisation['notleading'], show_alert=True)

@dp.callback_query_handler(game.filter(action=["next_word"]))
async def next_word(call: types.CallbackQuery):
    data = session.read_data()
    if(call.from_user.id == data['id_user']):
        await call.answer(function.new_word(), show_alert=True)
    else:
        await call.answer(localisation['notleading'], show_alert=True)
 
@dp.message_handler()
async def message_find(message: types.Message):
    data = session.read_data()
    if(message.chat.id == data['id_chat']):
        made_text = re.sub('ё', 'е', message.text.lower())
        made_text = re.sub('ъ', 'ь', made_text)
        word_text = re.sub('ё', 'е', data['word'])
        word_text = re.sub('ъ', 'ь', word_text)
        if(word_text in made_text):
            if(message.from_user.id != data['id_user']):
                function.update_user(message.from_user.id, data['id_chat']) 
                function.db_update_user(message.from_user.id, message.from_user.full_name) 
                await message.reply( f"{random.sample(localisation['win'], k=1)[0]} <b>{data['word']}</b>", parse_mode=types.ParseMode.HTML)
                await message.answer(f"<a href='{message.from_user.url}'>{message.from_user.first_name}</a> {localisation['describe_word']}", reply_markup=keyboard_add(), parse_mode=types.ParseMode.HTML)
            else:
                function.db_user_downgrade(message.from_user.id, message.from_user.full_name) 
                await message.reply( localisation['angry'], parse_mode=types.ParseMode.HTML)

if __name__ == '__main__':
    session.start_session()
    executor.start_polling(dp)
    
    