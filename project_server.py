#Yousif Ahmed Jassim 202010375 sec 1
#Hasan Ali Khalil Rajab 202100351 sec 1
import socket
import requests
import json
import threading

def fix_time(time): 
     # Function to fix the time format: ("2023-12-31T05:40:00+00:00" --> "5:40")
    if not time: return "None"   #sometimes [arrival][actual] is null from API
    time_string = time.split(":")
    hour = (time_string[0])[-2:]
    minutes = time_string[1]
    if hour[0] == "0": 
        hour = hour[1]
    return hour + ":" + minutes

def handle_client_request(client_socket, sock_address):
    # Function to handle client requests
    client_name = {sock_address: client_socket.recv(1024).decode('ascii')}
    print(f"{client_name[sock_address]} has connected, "
          f"From (ip, port):({sock_address[0]}, {sock_address[1]}).")

    while True:
        try: 
            # Receive client request
            request = client_socket.recv(1024).decode('ascii')
            # If request is 'e', send disconnection message and break the loop
            if request == "e":
                client_socket.send(("disconnecting from the server.").encode('ascii'))
                print(f'{client_name[sock_address]} has disconnected.')
                break
            
            response_json = {}
            response_list = []

            if request == 'a': # Request for all arrived flights
                for flight in data["data"]:
                    if flight["flight_status"] == "landed":
                       # print(flight["arrival"]["actual"])
                        #if not flight["arrival"]["actual"]: print(flight)
                        response = [
                            flight["flight"]["iata"],
                            flight["departure"]["airport"],
                            fix_time(flight["arrival"]["actual"]),
                            flight["arrival"]["terminal"],
                            flight["arrival"]["gate"]
                        ]
                        response_list.append(response)
                print((client_name[sock_address]), "requested all arrived flights.")
            
            
            elif request == 'b': # Request for all delayed flights
                for flight in data["data"]:
                    if flight["arrival"]["delay"]:
                        response = [
                            flight["flight"]["iata"],
                            flight["departure"]["airport"],
                            fix_time(flight["departure"]["scheduled"]),
                            fix_time(flight["arrival"]["estimated"]),
                            flight["arrival"]["delay"],
                            flight["arrival"]["terminal"],
                            flight["arrival"]["gate"]
                        ]
                        response_list.append(response)
                print((client_name[sock_address]), "requested all delayed flights.")
            
            elif request[0] == 'c': # Request for flights from a specific city code
                city_code = request[1:]
                for flight in data["data"]:
                    if flight["departure"]["iata"] == city_code:
                        response = [
                            flight["flight"]["iata"],
                            flight["departure"]["airport"],
                            fix_time(flight["departure"]["scheduled"]),
                            fix_time(flight["arrival"]["estimated"]),
                            flight["departure"]["gate"],
                            flight["arrival"]["gate"],
                            flight["flight_status"]
                        ]
                        response_list.append(response)

                print((client_name[sock_address]), "requested flights from:", city_code)
            
            elif request[0] == 'd': # Request for details of a specific flight
                flight_code = request[1:]
                for flight in data["data"]:
                    if flight["flight"]["iata"] == flight_code:
                        response = [
                            flight["flight"]["iata"],
                            flight["departure"]["airport"],
                            flight["departure"]["gate"],
                            flight["departure"]["terminal"],
                            flight["arrival"]["airport"],
                            flight["arrival"]["gate"],
                            flight["arrival"]["terminal"],
                            flight["flight_status"],
                            fix_time(flight["departure"]["scheduled"]),
                            fix_time(flight["arrival"]["scheduled"])
                        ]
                        response_list.append(response)
                print((client_name[sock_address]),
                       "requested details of the flight:", flight_code)
            
            response_json["flight"] = response_list
            # sending the response in json format
            client_socket.sendall((json.dumps(response_json)).encode('ascii'))
            
        except (socket.error, ConnectionResetError): 
            # Catch socket errors and handle disconnection
            print(f"{client_name[sock_address]} has disconnected.")
            break
    
    client_socket.close()

###############################################################################

# Get airport icao code from user
airport_code = input("Choose an airport (ICAO) code: ").upper()
params = {
    'access_key': 'dcde146b78bbf011a305dcb511911ddf',
    'limit': 100,
    'arr_icao': airport_code
}
# Make API request to retrieve flight data
api_response = requests.get('http://api.aviationstack.com/v1/flights?', params)

# Save API response to a JSON file
with open("group_GC1.json", "w") as json_file:
    json.dump(api_response.json(), json_file, indent=4)

# Load flight data from JSON file
with open("group_GC1.json", "r") as f:
    data = json.load(f)

print("Server is ready to accept connections from clients")

# configure server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "127.0.0.1"
server_port = 49994
server_socket.bind((server_ip, server_port))
server_socket.listen(3)

while True:
    # Accept client connections
    client_socket, sock_address = server_socket.accept()
    # Create a new thread for each client
    client_Thread = threading.Thread(target=handle_client_request,
                                     args=(client_socket, sock_address))
    client_Thread.start()