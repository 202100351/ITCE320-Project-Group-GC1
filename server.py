import socket
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(("127.0.0.1", 49999))
ss.listen(5)
cs, sockaddress = ss.accept()
print('Accepted request from', sockaddress[0] ,'with port number', sockaddress[1])
msg = (cs.recv(1024)).decode('ascii')
cs.send(("server>>:hello "+msg).encode('ascii'))

while True:
  
   ss.listen(20)
   for i in range(10):
    msg = (cs.recv(1024)).decode('ascii')
    cs.send(("server>>:").encode('ascii')) 

   if msg.decode('asci')== 'bye':
      cs.send(("server>>:good"+msg).encode('ascii'))
      break
   


cs.close()
ss.close()