import socket
import requests
import json

airport_code = input("Choose an airport (icao) code: ")

params = {'access_key':'ff1a4156d990b500005ee6d92ed4a4ae',
          'limit':100,
          'arr_icao':airport_code}

api_response = requests.get('http://api.aviationstack.com/v1/flights?',params)

with open("group_GC1.json", mode="w") as jsonfile:
  json.dump(api_response.json(),jsonfile, indent=4)

with open("group_GC1.json", mode="r") as f:
  data = json.load(f)
#######################################################################################
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(("127.0.0.1", 49994))
ss.listen(1)
cs, sockaddress = ss.accept()
client = {sockaddress:cs.recv(1024).decode('ascii')}
print('Accepted request from', sockaddress[0] ,'with port number', sockaddress[1])
print(f'{client[sockaddress]} has connected.')
while True:
 try:
  msg = (cs.recv(1024)).decode('ascii')
  if msg== 'bye'or msg== 'quit':
       cs.send(("server>>:good"+msg).encode('ascii'))
       print(f'{client[sockaddress]} has disconnected.')
       break
 except (socket.error, ConnectionResetError):
            print(f"{client[sockaddress]} has disconnected.")
            break
 print(msg,"has been sent.")
 cs.send((msg.upper()).encode('ascii'))

cs.close()
ss.close()