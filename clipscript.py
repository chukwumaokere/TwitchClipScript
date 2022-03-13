'''Pinot's Clip Script'''
from twitch_chat import TwitchChat
from pynput.keyboard import Key, Controller
import tkinter as tk
import sys 
import threading

class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(tk.END, text) # write text to textbox
            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass

keyboard = Controller();

root= tk.Tk()
root.title('Pinot\'s Clip Bot')

canvas1 = tk.Canvas(root, width = 300, height = 300, relief= 'raised')
canvas1.pack()

label1 = tk.Label(root, text='Pinot\'s Clip Bot')
label1.config(font=('helvetica', 14))
canvas1.create_window(150, 25, window=label1)

label2 = tk.Label(root, text='Channel Name:')
label2.config(font=('helvetica', 10))
canvas1.create_window(150, 50, window=label2)
channel_name = tk.Entry (root) 
canvas1.create_window(150, 70, window=channel_name)

label3 = tk.Label(root, text='Bot Name:')
label3.config(font=('helvetica', 10))
canvas1.create_window(150, 100, window=label3)
bot_name = tk.Entry (root) 
canvas1.create_window(150, 120, window=bot_name)

label4 = tk.Label(root, text='Auth Token:')
label4.config(font=('helvetica', 10))
canvas1.create_window(150, 150, window=label4)
token = tk.Entry (root) 
canvas1.create_window(150, 170, window=token)

mybot = None

def connect():
    TOKEN = token.get()
    BOT_NICKNAME = bot_name.get()
    CHANNEL = f'#{channel_name.get()}'
    print(f'Connecting to {CHANNEL}\'s chat as {BOT_NICKNAME}')
    global mybot
    mybot = TwitchChat(oauth=TOKEN, bot_name=BOT_NICKNAME, channel_name=CHANNEL)
    while True:
        user, message = mybot.listen_to_chat()
        if message: 
            print(f'[INCOMING MESSAGE] - User: {user}, Message: {message}')
            if message == '!clip':
                print('Clip command received making clip')
                mybot.send_to_chat(f'{BOT_NICKNAME} here! Clip command recieved! Making clip...')
                keyboard.press(Key.f8)
                keyboard.release(Key.f8)
def close():
    global mybot
    print('Closing connection. Goodbye!')
    mybot.close_socket()

def start_connection():
    t = threading.Thread(target=connect)
    t.start()

button1 = tk.Button(text='Start',command=start_connection, bg='green',fg='white')
button2 = tk.Button(text='Stop',command=close, bg='brown',fg='white')
canvas1.create_window(150, 220, window=button1)
canvas1.create_window(150, 250, window=button2)

t = tk.Text()
t.pack()
# create instance of file like object
pl = PrintLogger(t)

# replace sys.stdout with our object
sys.stdout = pl

root.mainloop() 
