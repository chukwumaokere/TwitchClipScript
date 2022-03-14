'''Pinot's Clip Script'''
from typing import Dict
from twitch_chat import TwitchChat
from pynput.keyboard import Key, Controller
import tkinter as tk
import sys 
import threading
import webbrowser
from configparser import ConfigParser

# To print logs in window
class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(tk.END, text) # write text to textbox
            # could also scroll to end of textbox here to make sure always visible
        self.textbox.see(tk.END) # scroll to end

    def flush(self): # needed for file like object
        pass

# Start values
config = ConfigParser()
keyboard = Controller()
mybot = None

# Window definitions
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 300
CENTER = WINDOW_WIDTH / 2
STARTING_POINT = 50

# tkinter stuff
root= tk.Tk()
root.title('Pinot\'s Clip Bot')

canvas1 = tk.Canvas(root, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, relief= 'raised')
canvas1.pack()

label1 = tk.Label(root, text='Pinot\'s Clip Bot')
label1.config(font=('helvetica', 18))
canvas1.create_window(CENTER, 25, window=label1)

label2 = tk.Label(root, text='Twitch Channel Name:')
label2.config(font=('helvetica', 10))
canvas1.create_window(CENTER, STARTING_POINT, window=label2)
channel_name = tk.Entry (root) 
canvas1.create_window(CENTER, STARTING_POINT+20, window=channel_name)

label3 = tk.Label(root, text='Bot Name:')
label3.config(font=('helvetica', 10))
canvas1.create_window(CENTER, STARTING_POINT * 2, window=label3)
bot_name = tk.Entry (root) 
canvas1.create_window(CENTER, STARTING_POINT * 2 + 20, window=bot_name)

label4 = tk.Label(root, text='Auth Token:')
label4.config(font=('helvetica', 10))
canvas1.create_window(CENTER, STARTING_POINT * 3, window=label4)
token = tk.Entry (root) 
canvas1.create_window(CENTER, STARTING_POINT * 3 + 20, window=token, width=300)

label5 = tk.Label(root, text='Key to press:')
label5.config(font=('helvetica', 10))
canvas1.create_window(CENTER, STARTING_POINT * 4, window=label5)
keypress = tk.Entry (root) 
canvas1.create_window(CENTER, STARTING_POINT * 4 + 20, window=keypress)

# Button functions
def connect():
    close()
    # Grab values
    TOKEN = token.get()
    BOT_NICKNAME = bot_name.get()
    CHANNEL_STRING = channel_name.get()
    CHANNEL = f'#{CHANNEL_STRING}'
    KEYPRESS_STRING = keypress.get().lower()
    KEYPRESS = Key[KEYPRESS_STRING]

    # Create a config or overwrite settings with new data
    create_config(CHANNEL_STRING, BOT_NICKNAME, TOKEN, KEYPRESS_STRING)
    print(f'Connecting to {CHANNEL}\'s chat as {BOT_NICKNAME}')

    # connect
    global mybot
    mybot = TwitchChat(oauth=TOKEN, bot_name=BOT_NICKNAME, channel_name=CHANNEL)
    while True:
        user, message = mybot.listen_to_chat()
        if message: 
            print(f'[INCOMING MESSAGE] - User: {user}, Message: {message}')
            if message == '!clip':
                print('Clip command received making clip')
                mybot.send_to_chat(f'{BOT_NICKNAME} here! Clip command recieved! Making clip...')
                keyboard.press(KEYPRESS)
                keyboard.release(KEYPRESS)

def close():
    global mybot
    print('Closing any previously open connections...')
    try:
        mybot.close_socket()
        print('Closing connection. Goodbye!')
        mybot = None
    except Exception:
        print(f'{Exception} No previous connections. Continuing...')
        mybot = None

def start_connection():
    thread = threading.Thread(target=connect)
    thread.start()

def callback(url):
    webbrowser.open_new(url)

def create_config(channel_name, bot_name, auth_token, key_to_press):
    print('Saving config info to config.ini...')
    config = ConfigParser()
    config.add_section('main')
    config.set('main', 'channel_name', channel_name)
    config.set('main', 'bot_name', bot_name)
    config.set('main', 'auth_token', auth_token)
    config.set('main', 'key_to_press', key_to_press)

    with open('config.ini', 'w') as f:
        config.write(f)
    print('Saved config file config.ini successfully!')

def read_config():
    print('Loading config file config.ini...')
    try: 
        config = ConfigParser()
        config.read('config.ini')
        channel_name.insert(0, config.get('main', 'channel_name'))
        bot_name.insert(0, config.get('main', 'bot_name'))
        token.insert(0, config.get('main', 'auth_token'))
        keypress.insert(0, config.get('main', 'key_to_press'))
        print('Loaded config file config.ini successfully!')
    except Exception:
        print(f'{Exception}: could not read config file. Starting fresh')

# Start and Stop buttons
button1 = tk.Button(text='Start/Restart',command=start_connection, bg='green',fg='white')
button2 = tk.Button(text='Stop',command=close, bg='brown',fg='white')
canvas1.create_window(CENTER, STARTING_POINT * 5 + 10, window=button1)
canvas1.create_window(CENTER, STARTING_POINT * 5 + 40, window=button2)

# Auth token link
link1 = tk.Label(root, text="Click Here To Get an Auth Token", fg="blue", cursor="hand2")
link1.pack()
link1.bind("<Button-1>", lambda e: callback("https://twitchapps.com/tmi"))

# Instructions
""" instruct_header = tk.Label(root, text='Instructions (if it isnt obvious :)')
instruct_header.config(font=('helvetica', 14))
instruct_header.pack();
instruct1 = tk.Label(root, text='1. Get an Auth Token from TMI (The link below)')
instruct1.config(font=('helvetica', 12))
instruct1.pack();
instruct2 = tk.Label(root, text='2. Fill out the input boxes above')
instruct2.config(font=('helvetica', 12))
instruct2.pack();
instruct3 = tk.Label(root, text='3. Press Start')
instruct3.config(font=('helvetica', 12))
instruct3.pack(); """

# Event log
eventlog = tk.Label(root, text='Event Log Below:')
eventlog.config(font=('helvetica', 14))
eventlog.pack();

t = tk.Text()
t.pack()
# create instance of file like object
pl = PrintLogger(t)

# replace sys.stdout with our object
sys.stdout = pl

# try to read config and insert values
read_config()

root.mainloop()