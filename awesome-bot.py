import re
import socket
import sys
import threading
from random import randint

host = 'irc.freenode.org'
port = 6667
nick = 'gabe_the_dog'
real_name = 'Gabe the dog'
channel = '#spbnet'
size = 2048

youtube_prefix = 'https://www.youtube.com/watch?v='
gabe_the_dog_sources = [
    'i1H0leZhXcY',
    'i11RMG_U3R4',
    'xK6cUQQ9cJY',
    'b2p8Zxmuq4g',
    'iY4Ci0wg258',
    'd6ysCgOu8N8',
    'dvZGs9QRNIw',
    'TsIZG5QbS1g',
    'gwkRRED5WxY',
    'oFRSLqpq9xk',
    'h4-pHUVthf0',
    'gIx6_Srsrog',
    'eWu5eB62dT8',
    'vwGnXKNGjT0',
    'AeEH5ugJrUU',
    'WCFnvj4Lztg',
    'Gl1uq4tg7YU',
    'rcIpIw4YtZk',
    '9u9vlj8CgS0',
    'gvOWADwCDNg',
    'JtA_WnBP_Co',
    'R78ZxZW_N-o',
    'd1lth7uX02g',
    'onZcB3y2RTM',
    'j20cTvQYe6s',
    'tVznLG3PAdM',
    'muLAN-kP5pE',
    'VJxNv2m7qns',
    'y3PcelCeraw'
]


def send_cmd(sock, cmd):
    sock.send(bytes(cmd))


def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def login(sock):
    send_cmd(sock, "USER {0} * * :{1}\r\n".format(nick, real_name))
    send_cmd(sock, "NICK {0}\r\n".format(nick))
    send_cmd(sock, "JOIN {0}\r\n".format(channel))


def send_msg(sock, msg):
    send_cmd(sock, "PRIVMSG {} :{}\r\n".format(channel, msg))


# magic

def magic(sock):
    index = randint(0, len(gabe_the_dog_sources) - 1)
    msg = "Check this out: {}{}".format(youtube_prefix, gabe_the_dog_sources[index])
    send_msg(sock, msg)


# thread routines

def send_routine(sock):
    while True:
        msg = raw_input()
        if msg.startswith("/q"):
            send_cmd(sock, "QUIT")
            sock.close()
            return
        send_msg(sock, msg)


def receive_routine(sock):
    try:
        while True:
            text = str(sock.recv(size))
            if text.startswith("PING "):
                send_cmd(sock, "PONG {}".format(text[5:]))
                continue
            if len(text) > 1:
                print_message(text, "PRIVMSG" in text and channel in text)
                if "show some magic" in text and nick in text:
                    magic(sock)
    except:
        print("Disconnected!")


def print_message(msg, is_private):
    if is_private:
        sender_nick = re.sub(r":(.*)!.*PRIVMSG " + channel + r" :(.*)", r"\1", msg)
        msg_text = re.sub(r":(.*)!.*PRIVMSG " + channel + r" :(.*)", r"\2", msg)
        print("<{}>: {}".format(sender_nick[:-1], msg_text[:-1]))
    else:
        print(msg)


def main():
    sock = connect()
    login(sock)
    print("Connected!")
    sender_thread = threading.Thread(target=send_routine, args=(sock,))
    receiver_thread = threading.Thread(target=receive_routine, args=(sock,))
    sender_thread.start()
    receiver_thread.start()
    sender_thread.join()
    receiver_thread.join()


main()
