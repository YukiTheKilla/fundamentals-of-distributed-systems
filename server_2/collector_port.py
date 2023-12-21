import socket
import os

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 1111))
    server_socket.listen(1)

    print(f"Server listening on 1111")

    while True:
        conn, addr = server_socket.accept()
        print(f'Connection from {addr}')

        receive_and_save_data(conn)

def receive_and_save_data(client_socket):
    # Receive data as binary
    received_data = b''
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        received_data += chunk

    # Find the index of '[' to determine the end of the file name
    index_of_bracket = received_data.find(b'[')
    if index_of_bracket != -1:
        file_name = received_data[:index_of_bracket].decode('utf-8').strip()
        print(f'File name: {file_name}')
        
        json_output_path1 = os.path.join('server_2/result', file_name)
        os.makedirs(os.path.dirname(json_output_path1), exist_ok=True)

        # Save the remaining data after '[' to the file
        with open(json_output_path1, 'wb') as file:
            file.write(received_data[index_of_bracket:])
        
        print(f'Data received and saved as {os.path.basename(json_output_path1)}.')

    else:
        print('Invalid data format. Missing "[" character.')

    client_socket.close()

def forward_data(data, forward_port):
    forward_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    forward_socket.connect(('127.0.0.1', forward_port))
    forward_socket.sendall(data)
    forward_socket.close()

if __name__ == '__main__':
    start_server()
