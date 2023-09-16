import socket
import time
import threading

def simulate_weighbridge_data(client_socket):
    while True:
        data_to_send = str(time.time()) 
        client_socket.send(data_to_send.encode())
        print(f"Sent data: {data_to_send}")
        time.sleep(0.1)  # Simulate data being sent every 0.1 seconds

def main():
    server_ip = '127.0.0.1'  # Replace with the desired server IP address
    server_port = 12346  # Replace with the desired server port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)  # Listen for one incoming connection

    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        
        # Start a new thread to simulate RFID data for this client
        threading.Thread(target=simulate_weighbridge_data, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
