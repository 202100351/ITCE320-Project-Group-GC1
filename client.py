import socket
cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cs.connect(("127.0.0.1",49999))

while True:
 msg = input(":" )
 cs.send(msg.encode('ascii'))
 data =cs.recv(1024)
 print(data.decode('ascii'))
 if data.decode('ascii')== 'server>>:goodbye':
  print("server disconnected")
  break


cs.close()
