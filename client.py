import socket  # socket module, מודול תקשורת

c = socket.socket()  # c-client socket, create a channel, יצירת ערוץ תקשורת
c.connect(('127.0.0.1', 1729))  # התחברות לשרת

while True:
    send = input("enter\n")
    c.send(send.encode())
    if send == "EXIT":
        break
    if send == "SCRN":
        pic = open("new.jpg", 'wb')
        num_chunks = int(c.recv(1024).decode())
        for i in range(0, num_chunks):
            chunk = c.recv(1024)
            pic.write(chunk)
        pic.close()
    else:
        data = c.recv(1024).decode()  # קבלת מידע מהשרת
        print(data)  # הדפסת מידע מהשרת
c.close()  # סגירת השרת
