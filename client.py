import socket
cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cs.connect(("127.0.0.1",49999))
name = input("username:" )
for i in range(20):
 #name = input(":" )
 cs.send(name.encode('ascii'))
 msg =cs.recv(1024)
 print(msg.decode('ascii'))
 name = input(":" )

cs.close()
