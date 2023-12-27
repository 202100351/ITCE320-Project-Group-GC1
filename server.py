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
print("Server is ready to accept connection from clients")
###############################################################################
ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(("127.0.0.1", 49994))
ss.listen(1)
cs, sockaddress = ss.accept()
client = {sockaddress:cs.recv(1024).decode('ascii')}
print('Accepted request from', sockaddress[0] ,'with port number', sockaddress[1])
print(f'{client[sockaddress]} has connected.')
while True:
 try:
  count=0
  msg = (cs.recv(1024)).decode('ascii')
  if msg== 'bye'or msg== 'quit'or msg=="e":
       cs.send(("disconnecting from the server.").encode('ascii'))
       print(f'{client[sockaddress]} has disconnected.')
       break
  if msg =='a'or msg=='arrived':
     mylist=[]
     dictionary= {}
     for flight in data["data"]:
     
      if flight["flight_status"]=="landed":
       response=[]
       fiata=flight["flight"]["iata"]
       fdport=flight["departure"]["airport"]
       farrtime=flight["arrival"]["actual"]
       farrt=flight["arrival"]["terminal"]
       farrg=flight["arrival"]["gate"]
       
       response.extend([fiata,fdport,farrtime,farrt,farrg])
       
       mylist.append(response)
       dictionary["flight"]=mylist
       count+=1
     cs.sendall((json.dumps(dictionary)).encode('ascii'))
       
     print((count))
  if msg=='b':
     mylist=[]
     dictionary= {}
     for flight in data["data"]:
     
      if flight["arrival"]["delay"]:
       response=[]
       fiata=flight["flight"]["iata"]
       fdport=flight["departure"]["airport"]
       fdtime=flight["departure"]["scheduled"]
       farrtime=flight["arrival"]["estimated"]
       farrdelay=flight["arrival"]["delay"]
       farrt=flight["arrival"]["terminal"]
       farrg=flight["arrival"]["gate"]
       
       response.extend([fiata,fdport,fdtime,farrtime,farrdelay,farrt,farrg])
       
       mylist.append(response)
       dictionary["flight"]=mylist
       count+=1
     cs.sendall((json.dumps(dictionary)).encode('ascii'))
       
     print((count))
 
  if msg=='c':
     mylist=[]
     dictionary= {}
     City_code = (cs.recv(1024)).decode('ascii')
     for flight in data["data"]:
     
      if flight["departure"]["iata"]== City_code:
       response=[]
       fiata=flight["flight"]["iata"]
       fdport=flight["departure"]["airport"]
       fdtime=flight["departure"]["scheduled"]
       farrtime=flight["arrival"]["estimated"]
       fdg=flight["departure"]["gate"]
       farrg=flight["arrival"]["gate"]
       fstatus= flight["flight_status"]
       response.extend([fiata,fdport,fdtime,farrtime,fdg,farrg,fstatus])
       
       mylist.append(response)
       dictionary["flight"]=mylist
       count+=1
     cs.sendall((json.dumps(dictionary)).encode('ascii'))
       
     print((count))
     
  if msg=='d':
     mylist=[]
     dictionary= {}
     flight_code = (cs.recv(1024)).decode('ascii') 
     for flight in data["data"]:
      if flight["flight"]["iata"]== flight_code:
      
       response=[]
       fiata=flight["flight"]["iata"]
       fdport=flight["departure"]["airport"]
       fdg=flight["departure"]["gate"]
       fdt=flight["departure"]["terminal"]
       farrport=flight["arrival"]["airport"]
       farrg=flight["arrival"]["gate"]
       farrt=flight["arrival"]["terminal"]
       fstatus= flight["flight_status"]
       fdtime=flight["departure"]["scheduled"]
       farrtime=flight["arrival"]["scheduled"]
       
       response.extend([fiata,fdport,fdg,fdt,farrport,farrg,farrt,fstatus,fdtime,farrtime])
       
       mylist.append(response)
       dictionary["flight"]=mylist
       count+=1
     cs.sendall((json.dumps(dictionary)).encode('ascii'))
       
     print((count)) 


 except (socket.error, ConnectionResetError):
            print(f"{client[sockaddress]} has disconnected.")
            break

cs.close()
ss.close()
###############################################################################