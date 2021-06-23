import socket
import datetime
import random
import os
from PIL import ImageGrab
import math
import subprocess
from shutil import copy2

s = socket.socket()
s.bind(('127.0.0.1', 1729))
s.listen()
(c, address) = s.accept()

data = ""
while data != "EXIT":
    data = c.recv(1024).decode()
    if data == "RAND":
        c.send(str(random.randint(1, 11)).encode())
    elif data == "TIME":
        c.send(("the time is: {}".format(datetime.datetime.now()).encode()))
    elif data == "COMP":
        c.send(socket.gethostname().encode())
    elif data == "ADDR":
        c.send(socket.gethostbyname(socket.gethostname()).encode())
    elif data[0:4] == "FLDR":
        try:
            c.send(",".join(os.listdir(data[5::])).encode())
        except FileNotFoundError:
            c.send("wrong path".encode())
    elif data == 'SCRN':
        im = ImageGrab.grab()
        im.save('pic.jpg')
        size = os.path.getsize('pic.jpg')
        num_chunks = math.ceil(size / 1024)
        c.send(str(num_chunks).encode())
        pic = open("pic.jpg", "rb")
        for i in range(0, num_chunks - 1):
            chunk = pic.read(1024)
            c.send(chunk)
        chunk = pic.read()
        c.send(chunk)
        pic.close()
    elif data[0:4] == 'EXEC':
        result = subprocess.run(['where', data[5::]], stdout=subprocess.PIPE)

        path = result.stdout.decode('utf-8')
        print(path)
        if path == "":
            c.send("wrong path".encode())
        else:
            os.startfile(path.split("\r\n")[0])
            c.send("opened".encode())
    elif data[0:4] == 'DELE':
        print(data[5::])

        os.remove(data[data.find("C")::].replace(r"\u202a", ""))
        c.send("removed".encode())

    elif data[0:4] == 'COPY':
        path = data.replace(r"\u202a", "")
        path = path.split(" ")
        print(path)
        if os.path.exists(path[1]):
            copy2(path[1], path[2])
            c.send("copied".encode())
        else:
            c.send("wrong path".encode())


    else:
        c.send("invalid command".encode())

c.close()
s.close()
