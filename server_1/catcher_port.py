import socket
import os

def start_receiver():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind(('127.0.0.1', 111))
    receiver_socket.listen(1)

    print(f"Receiver listening on 111")

    while True:
        conn, addr = receiver_socket.accept()
        print(f'Connection from {addr}')

        received_data = receive_data(conn)
        save_received_data(received_data)

def receive_data(client_socket):
    received_data = b''
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        received_data += chunk

    client_socket.close()
    return received_data

def save_received_data(data):
    # Find the index of '[' to determine the end of the file name
    index_of_bracket = data.find(b'[')
    if index_of_bracket != -1:
        # Extract the file name
        file_name = data[:index_of_bracket].decode('utf-8').strip()
        print(f'File name: {file_name}')

        result_dir = os.path.join(os.path.dirname(__file__), 'result')
        os.makedirs(result_dir, exist_ok=True)

        file_path = os.path.join(result_dir, file_name)

        # Save the remaining data after '[' to the file
        with open(file_path, 'wb') as file:
            file.write(data[index_of_bracket:])

        print(f'Received data saved as {file_name} in the "result" directory.')
    else:
        print('Invalid data format. Missing "[" character.')

if __name__ == '__main__':
    start_receiver()
