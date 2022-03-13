'''Mingo Clip Script'''
from config import CHANNEL, TOKEN, BOT_NICKNAME
from twitch_chat import TwitchChat
from pynput.keyboard import Key, Controller

keyboard = Controller();

mybot = TwitchChat(oauth=TOKEN, bot_name=BOT_NICKNAME, channel_name=CHANNEL)

while True:
    user, message = mybot.listen_to_chat()
    if message: 
        print(f'[INCOMING MESSAGE] - User: {user}, Message: {message}')
        if message == '!clip':
            print('Clip command received making clip')
            mybot.send_to_chat(f'{BOT_NICKNAME} here! Clip command recieved! Making clip...')
            keyboard.press(Key.f11)
            keyboard.release(Key.f11)
