import socket
import json
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as cs:
 cs.connect(("127.0.0.1",49994))
 msg = input(":" )
 cs.send(msg.encode('ascii'))
 while True: 

  print("\nOptions:") 
  print("a. Arrived flights")
  print("b. Delayed flights")
  print("c. Incoming Flights from a city")
  print("d. Details of a flight")
  print("e. Quit")
  
  option=input(msg+ " Select an option: ")
  if option =='a':
   cs.send(option.encode("ascii"))
   recv=cs.recv(20000)
   words = json.loads(recv.decode("ascii"))
   for flight in words["flight"]:
    #print(flight)
    print(f"iata:{flight[0]}, Dep_airport:{flight[1]}, Arr_time:{flight[2]}, Terminal:{flight[3]}, Gate:{flight[3]}")
  
  
  if option =='b':
   cs.send(option.encode("ascii"))
   recv=cs.recv(20000)
   words = json.loads(recv.decode("ascii"))
   for flight in words["flight"]:
    #print(flight)
    print(f"iata:{flight[0]}, Dep_airport:{flight[1]}, Dep_time:{flight[2]}")
    print(f"Est_arr_time:{flight[3]}, Delay:{flight[4]}, Terminal:{flight[5]}, Gate:{flight[6]}")
    print()
  
  if option =='c':
   try:
    City_code = input("City code (IATA): ")
    cs.send(option.encode("ascii"))
    cs.send(City_code.encode("ascii"))
    recv=cs.recv(20000)
    words = json.loads(recv.decode("ascii"))
    for flight in words["flight"]:
      print(f"iata:{flight[0]}, Dep_airport:{flight[1]}, Dep_time:{flight[2]}")
      print(f"Est_arr_time:{flight[3]}, Dep Gate:{flight[4]}, Arrival Gate:{flight[5]}, Status:{flight[6]}")
      print()
   except(KeyError):print(f"No flights coming from:{City_code}")
  if option =='d':
   try:
    flight_code = input("IATA: ")
    cs.send(option.encode("ascii"))
    cs.send(flight_code.encode("ascii"))
    recv=cs.recv(20000)
    words = json.loads(recv.decode("ascii"))
    for flight in words["flight"]:
      print(f"iata:{flight[0]}, Dep_airport:{flight[1]}, Dep Gate:{flight[2]}, Dep Terminal:{flight[3]}")
      print(f"Arr_airport:{flight[4]}, Arr Gate:{flight[5]}, Arr Terminal:{flight[6]}")
      print(f"Status:{flight[7]}, schedueld dep time:{flight[8]}, schedueld arr time:{flight[9]}")
   except(KeyError):print(f"No flights with this iata code:{flight_code}")
  
  
  if option =='e':
   cs.send(option.encode("ascii"))
   recv=cs.recv(1024).decode("ascii")
   print(recv) 
   break
