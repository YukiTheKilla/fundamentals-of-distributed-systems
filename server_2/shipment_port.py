import socket
import os

def send_file(client_socket, file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
        client_socket.send(file_data)

def start_server():
    base_path = os.path.dirname(__file__)
    folder_path = 'server_2/result'
    full_path = os.path.join(base_path, folder_path)
    
    host = '127.0.0.1'  # localhost
    port = 3333

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {port}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            file_name = client_socket.recv(1024).decode('utf-8')
            print(f"Received file name: {file_name}")

            # Construct the full path to the file
            file_path = os.path.join(full_path, file_name)

            if os.path.exists(file_path):
                # Send the file to the client
                send_file(client_socket, file_path)
                print(f"Sent file: {file_path}")
            else:
                error_message = "File not found in the specified folder."
                client_socket.send(error_message.encode('utf-8'))
                print(error_message)

            client_socket.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_server()
