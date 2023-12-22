import socket
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(("127.0.0.1", 49999))
ss.listen(3)
cs, sockaddress = ss.accept()
print('Accepted request from', sockaddress[0] ,'with port number', sockaddress[1])
 
while True:
 msg = (cs.recv(1024)).decode('ascii')
 if msg== 'bye':
      cs.send(("server>>:good"+msg).encode('ascii'))
      break
 cs.send(("server>>:"+msg).encode('ascii'))
ss.listen(5)



cs.close()
ss.close()