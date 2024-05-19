import time
import socket
import new_space1  # Import space1 module
import new_space2  # Similarly import other space modules
import new_space3
import new_space4

# List of space modules for each parking space
spaces = [new_space1, new_space2, new_space3, new_space4]

# Define identifiers
carparkname = 'A' 
car_park_location = (4,7) # (x,y) coordinates

# Track previous status for each space
previous_statuses = [None] * len(spaces)

SERVER_IP = '192.168.1.105'  # Replace with laptop's IP address
SERVER_PORT = 12345

def connect_to_server():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, SERVER_PORT))
            print("Connected to server at {}:{}".format(SERVER_IP, SERVER_PORT))
            
            location_message = f"{carparkname}:LOCATION:{car_park_location[0]},{car_park_location[1]}"
            client_socket.send(location_message.encode('utf-8'))
            print(f"Sent location to server: {location_message}")
            
            return client_socket
        except Exception as e:
            print("Error: Failed to connect to server, retrying in 5 seconds:", e)
            time.sleep(5)

client_socket = connect_to_server()

try:
    while True:
        for i, space in enumerate(spaces, 1):
            try:
                status = space.get_led_status()
                print(f"Parking Space {i} Status:", status)

                # Check if the status has changed
                if status != previous_statuses[i - 1]:
                    previous_statuses[i - 1] = status
                    carparkbay = i
                    message = f"{carparkname}-{carparkbay}: {status}"
                    if client_socket is None:
                        client_socket = connect_to_server()
                    try:
                        client_socket.send(message.encode('utf-8'))
                        print(f"Sent status to server: {message}")
                    except Exception as e:
                        print(f"Error: Failed to send status to server: {e}")
                        client_socket.close()
                        client_socket = None
                        client_socket = connect_to_server()
            except Exception as e:
                print(f"Error: Failed to get status from space {i}:", e)

        time.sleep(1)  # Adjust as needed for the desired update frequency

except KeyboardInterrupt:
    print("Stopping all processes...")
    for space in spaces:
        space.GPIO.cleanup()  # Clean up GPIO on exit
    if client_socket:
        client_socket.close()
    print("All processes stopped.")
