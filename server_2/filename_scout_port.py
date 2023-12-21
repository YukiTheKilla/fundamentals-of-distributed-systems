import os
import json
import socket
    
# Function to find all files in a folder
def find_all_files(folder_path):
    all_files = os.listdir(folder_path)
    return all_files

# Function to handle client requests
def handle_client(client_socket, folder_path):
    # Find all files in the specified folder
    all_files = find_all_files(folder_path)

    # Print the list of files on the server side
    print("List of files in the folder on the server:")
    for file in all_files:
        print(file)

    # Convert the list to JSON format
    json_data = json.dumps(all_files)

    # Send the JSON data to the client
    client_socket.send(json_data.encode())

# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 2222))
    server.listen(5)

    print("Server listening on port 2222")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'result'))

        # Handle the client request
        handle_client(client_socket, folder_path)

        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    main()
