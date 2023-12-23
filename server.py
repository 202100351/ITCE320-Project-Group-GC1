import socket
import requests
import json



params = {'access_key':'ff1a4156d990b500005ee6d92ed4a4ae',
          'limit':20}

api_response = requests.get('http://api.aviationstack.com/v1/flights?',params)
json_result = json.dumps(api_response.json(),indent=4)


print(json_result)
print(type(api_response))
print(type(json_result))





# ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# ss.bind(("127.0.0.1", 49994))
# ss.listen(3)
# cs, sockaddress = ss.accept()
# print('Accepted request from', sockaddress[0] ,'with port number', sockaddress[1])
 
# while True:
#  msg = (cs.recv(1024)).decode('ascii')
#  if msg== 'bye':
#       cs.send(("server>>:good"+msg).encode('ascii'))
#       break
#  print(msg,"has connected")
#  cs.send((msg).encode('ascii'))
#  ss.listen(5)
 

# cs.close()
# ss.close()