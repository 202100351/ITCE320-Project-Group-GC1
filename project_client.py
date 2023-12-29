import socket
import json

def send_receive_data(client_socket, data,parameter=""):
    # Function to send data to the server and receive the processed response
    if data == "c" or data == "d":
        data = data+parameter 
    client_socket.send(data.encode("ascii"))
    server_response = client_socket.recv(32768)
    processed_response = json.loads(server_response.decode("ascii"))
    return processed_response


def print_flight_details(flight):
    # Function to print flight details based on the selected option
    if option == "a":
         print(f"iata:{flight[0]}, Dep airport:{flight[1]}, Arr time:{flight[2]},"
               f" Terminal:{flight[3]}, Gate:{flight[4]}")
    elif option == "b":
        print(f"iata:{flight[0]}, Dep airport:{flight[1]},"
              f"Dep time:{flight[2]},Est arr time:{flight[3]}, "
              f"Delay:{flight[4]}, Terminal:{flight[5]}, Gate:{flight[6]}")
    
    
    elif option == 'c':
        print(f"\niata: {flight[0]},                 Departure airport: {flight[1]}")
        print(f"Departure time: {flight[2]},        Estimated arrival time: {flight[3]}")
        print(f"Departure Gate: {flight[4]},          Arrival Gate: {flight[5]}")
        print(f"Flight Status: {flight[6]}")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # configure client socket
        server_ip = "127.0.0.1"
        server_port = 49994
        client_socket.connect((server_ip, server_port))
        client_name = input("Name: ")
        client_socket.send(client_name.encode('ascii'))

        while True:
            print("\nOptions:")
            print("a. Arrived flights")
            print("b. Delayed flights")
            print("c. Incoming Flights from a city")
            print("d. Details of a flight")
            print("e. Quit")

            option = input(f"{client_name} Select an option (a-e): ")

            if option == 'e':
                client_socket.send(option.encode("ascii"))
                server_response = client_socket.recv(1024).decode("ascii")
                print(server_response)
                break

            if option == 'a':
                server_response = send_receive_data(client_socket, option)
                print(f"There is {len(server_response['flight'])} arrived flight.")
                for flight in server_response["flight"]:
                    print_flight_details(flight)

            elif option == 'b':
                server_response = send_receive_data(client_socket, option)
                print(f"There is {len(server_response['flight'])} delayed flight.")
                for flight in server_response["flight"]:
                    print_flight_details(flight)

            elif option == 'c':
                try:
                    city_code = input("City code (Airport IATA code): ")
                    server_response = send_receive_data(client_socket, option, city_code)
                    if len(server_response["flight"])== 0:
                        raise KeyError
                    print(f"There is {len(server_response['flight'])} flight coming from {city_code}")
                    for flight in server_response["flight"]:
                        print_flight_details(flight)
                
                except KeyError:
                    print(f"No flights coming from: {city_code}")

            elif option == 'd':
                try:
                    flight_code = input("IATA: ")
                    server_response = send_receive_data(client_socket, option, flight_code)
                    if len(server_response["flight"])== 0:
                        raise KeyError
                    for flight in server_response["flight"]:
                        print(f"\niata: {flight[0]}")
                        print(f"Departurr airport: {flight[1]}")
                        print(f"Departure Gate: {flight[2]}")
                        print(f"Departure Terminal: {flight[3]}")
                        print(f"Arrival airport: {flight[4]}")
                        print(f"Arrival Gate: {flight[5]}")
                        print(f"Arrival Terminal: {flight[6]}")
                        print(f"Flight Status: {flight[7]}")
                        print(f"Scheduled departure time: {flight[8]}")
                        print(f"Scheduled arriavl time: {flight[9]}")

                except KeyError:
                    print(f"No flights with this IATA code: {flight_code}")
            
            else:
                print("Invalid option choose from (a to e).")

except ConnectionRefusedError:
    print("Make sure to start the server first.")