import socket 
def send(sock, type):
    sock.send(type.encode("ascii"))

sock=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
address="192.168.1.10"
port=49999
sock.connect((address,port))
name=input("Enter your username")
sock.send(name.encode("ascii"))


while true: 

print("\nOptions:") 
print("a. Arrived flights")
print("b. Delayed flights")
print("c. Incoming Flights from a city")
print("d. Details of a flight")
print("e. Quit")

option=input("Select an option")
if option =='a':
send(sock,'arrived')
recv=sock.recv(1024)
print(recv.decode("ascii"))

if option=='b':
send(sock,'delayed')
recv=sock.recv(1024)
print(recv.decode("ascii"))

if option=='c':
from_city=input("Enter city")
send(sock,'city')
sock.send(from_city.encode("ascii"))
recv=sock.recv(1024)
print(recv.decode("ascii"))

if option=='d':
code=input("Enter flight code (IATA):")
send(sock,'detials')
sock.send(code.encode("ascii"))
recv=sock.recv(1024)
print(recv.decode("ascii"))

if choice == 'e':
send(sock, 'quit')

break

else:
print('Option is Invalid')

sock.close()

if __name__ == '__main__':
    main()
