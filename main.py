from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData
import logging, random, math, re, os
from localisation import localisation
from dotenv import load_dotenv

#import .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')
LANG = os.getenv('LANGUAGE')
TIME_DELTA = int(os.getenv('TIME_DELTA'))

#import Function
from function import Function
function = Function()

#import SessionHelper
from session import SessionHelper
session = SessionHelper()

#start aiogram
bot = Bot(token=TOKEN)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)

#command /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    me = await bot.get_me()
    await message.reply(f"{localisation[LANG]['start1']} /game@{me.username} {localisation[LANG]['start2']}")

#Callback_data to button
game = CallbackData("game", "action")

#keyboard with 2 button(see_word, next_word)
def keyboard_add():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text=localisation[LANG]['see_word'], callback_data=game.new(action="see_word")),
        types.InlineKeyboardButton(text=localisation[LANG]['next_word'], callback_data=game.new(action="next_word"))
    ]
    keyboard.add(*buttons)
    return keyboard

#command /info (debug)
@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    with open("info.json", "r") as file:
        lines =file.readlines()
        text = ''
        for line in lines:
            text += line
        await message.reply(text, disable_web_page_preview=True)

#command /game (start game)
@dp.message_handler(commands=['game'])
async def game_start(message: types.Message):
    #load session
    data = session.read_data()
    #check if the right chat
    if(int(message.chat.id) == int(data['id_chat'])):
        #check if can start a new game (not old session or time is over)
        if(data['id_user'] == 0 or not function.time_checker(data['time']) or data['word'] == ''):
            #new player
            function.update_user(message.from_user.id, message.from_user.first_name, data['id_chat']) 
            #send a word 
            await message.answer(f"<a href='{message.from_user.url}'>{message.from_user.first_name}</a> {localisation[LANG]['describe_word']}", reply_markup=keyboard_add(), parse_mode=types.ParseMode.HTML)
        else: 
            #time is not over
            await message.reply(f"{localisation[LANG]['gamestart_1']} {str(math.ceil((TIME_DELTA - function.delta_time(data['time']))/60))} {localisation[LANG]['gamestart_2']}")
    else:
        #send that this is not the right chat 
        await message.reply(localisation[LANG]['notchat'])

#stop game
@dp.message_handler(commands=['stop'])
async def rating(message: types.Message):
    #load session
    data = session.read_data()
    #check if the right chat
    if(int(message.chat.id) == int(data['id_chat'])):
        #check if this right user
        if(int(message.from_user.id) == int(data['id_user'])):
            function.reset_user()
            me = await bot.get_me()
            await message.reply( f"{localisation[LANG]['reset']} /game@{me.username}", parse_mode=types.ParseMode.HTML)
        else:
            await message.reply(localisation[LANG]['reset_error'])
    else:
        #send that this is not the right chat 
        await message.reply(localisation[LANG]['notchat'])

#rating player
@dp.message_handler(commands=['data'])
async def rating(message: types.Message):
    #load session
    data = session.read_data()
    #check if the right chat
    await message.reply(data)

#rating player
@dp.message_handler(commands=['rating'])
async def rating(message: types.Message):
    #load session
    data = session.read_data()
    #check if the right chat
    if(int(message.chat.id) == int(data['id_chat'])):
        #try get top of user or send error message
        try:
            await message.reply(f"<b>{localisation[LANG]['top']}</b> ???? \n\n{function.get_top()}", parse_mode=types.ParseMode.HTML)    
        except KeyError:
            await message.reply(f"{localisation[LANG]['error']} \n {KeyError}", parse_mode=types.ParseMode.HTML)
    else:
        #send that this is not the right chat 
        await message.reply(localisation[LANG]['notchat'])

#send a actual word
@dp.callback_query_handler(game.filter(action=["see_word"]))
async def see_word(call: types.CallbackQuery):
    #load session
    data = session.read_data()
    #check if the right chat
    if(int(call.from_user.id) == int(data['id_user'])):
        await call.answer(data['word'], show_alert=True)
    else:
        #send that this is not the right chat 
        await call.answer(localisation[LANG]['notleading'], show_alert=True)

#get a new word and send a actual word
@dp.callback_query_handler(game.filter(action=["next_word"]))
async def next_word(call: types.CallbackQuery):
    #load session
    data = session.read_data()
    #check if the right chat
    if(int(call.from_user.id) == int(data['id_user'])):
        await call.answer(function.new_word(), show_alert=True)
    else:
        #send that this is not the right chat 
        await call.answer(localisation[LANG]['notleading'], show_alert=True)
 

#AMC(All Message Checker)
@dp.message_handler()
async def message_find(message: types.Message):
    #load session
    data = session.read_data()
    #check if the right chat
    if(int(message.chat.id) == int(data['id_chat'])):
        if(message.from_user.id == data['id_user']):
            function.update_time()
        #split text to each word
        split_text = message.text.lower().split()
        for i in split_text:
            #data cleaning and standardization
            made_text = re.sub('[^\w-]', '', i)
            made_text = re.sub('[\d_]', '', made_text)
            made_text = re.sub('??', '??', made_text)
            made_text = re.sub('??', '??', made_text)
            word_text = re.sub('??', '??', data['word'])
            word_text = re.sub('??', '??', word_text)
            #check if this word is right
            if(word_text == made_text):
                #check if answer is not from the presenter
                if(message.from_user.id != data['id_user']):
                    #Send celebration
                    await message.reply(
                        f"{random.sample(localisation[LANG]['win'], k=1)[0]}<a href='{message.from_user.url}'>{message.from_user.first_name}</a> {localisation[LANG]['win_l'][0]} <b>{data['word']}</b> {localisation[LANG]['win_l'][1]} <a href='tg://user?id={data['id_user']}'>{data['name_user']}</a> {localisation[LANG]['win_l'][2]} {math.floor(function.delta_time(data['time']))} {localisation[LANG]['win_l'][3]}",
                        parse_mode=types.ParseMode.HTML)
                    #add +1 to rating
                    function.db_update_user(message.from_user.id, message.from_user.full_name) 
                    #new player
                    function.update_user(message.from_user.id, message.from_user.first_name, data['id_chat'] ) 
                    #Send a new word
                    await message.answer(f"<a href='{message.from_user.url}'>{message.from_user.first_name}</a> {localisation[LANG]['describe_word']}", reply_markup=keyboard_add(), parse_mode=types.ParseMode.HTML)
                else:
                    #add -1 to rating and angry message)
                    me = await bot.get_me()
                    if(not data['warning']):
                        function.db_user_downgrade(message.from_user.id, message.from_user.full_name) 
                        function.warning_user()
                        await message.reply( localisation[LANG]['angry'], parse_mode=types.ParseMode.HTML)
                    else:
                        function.reset_user()
                        await message.reply( f"{localisation[LANG]['reset']} /game@{me.username}", parse_mode=types.ParseMode.HTML)

if __name__ == '__main__':
    #start session
    session.start_session()
    #start bot
    executor.start_polling(dp, skip_updates=True)
    
    