import socket
from config import SERVER, PORT
from typing import Tuple

class TwitchChat:
    global SERVER
    global PORT
    def __init__(self, channel_name: str, bot_name: str, oauth: str = None):
        global SERVER
        global PORT

        self.sock = socket.socket()
        self.channel = channel_name
        self.sock.connect((SERVER, PORT))

        self.allowed_to_post = oauth or bot_name

        if self.allowed_to_post:
            self.sock.send(f"PASS {oauth}\n".encode('utf-8'))
            self.sock.send(f"NICK {bot_name}\n".encode('utf-8'))
            self.sock.send(f"JOIN {channel_name}\n".encode('utf-8'))
        else:
            self.sock.send(f"NICK {bot_name}\n".encode('utf-8'))
            self.sock.send(f"JOIN #{channel_name}\n".encode('utf-8'))
    
        loading = True
        while loading:
            read_buffer_join = self.sock.recv(2048).decode('utf-8')
            print(read_buffer_join)

            for line in read_buffer_join.split('\n')[0:-1]:
                # checks if loading is complete
                loading = 'End of /NAMES list' not in line

    def send_to_chat(self, message: str):
        """
        sends a message to twitch chat if it's possible
        :param message: message to send in twitch chat
        :return:
        """

        if self.allowed_to_post:
            self.sock.send(f"PRIVMSG {self.channel} :{message}\n".encode('utf-8'))
        else:
            raise RuntimeError('Bot has no permission to send messages. Get oauth token at http://twitchapps.com/tmi/')

    def listen_to_chat(self) -> Tuple[str, str]:
        """
        listens to chat and returns name and
        designed for endless loops with ping pong socket concept
        :return: user, message from chat or None
        """
        read_buffer = self.sock.recv(2048).decode('utf-8')
        for line in read_buffer.split('\r\n'):
            # ping pong to stay alive
            if 'PING' in line and 'PRIVMSG' not in line:
                self.sock.send("PONG\n".encode('utf-8'))

            # reacts at user message
            elif line != '':
                parts = line.split(':', 2)
                return parts[1].split('!', 1)[0], parts[2]
    
    def close_socket(self) -> bool:
        return self.sock.close()