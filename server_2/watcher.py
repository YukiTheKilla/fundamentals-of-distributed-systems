import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import socket
import os

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'modified':
            file_path = event.src_path
            print(f'File {file_path} has been modified. Sending to server...')
            send_file_to_server(file_path)

def send_file_to_server(file_path):
    file_name = os.path.basename(file_path)

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(('127.0.0.1', 111))

                client_socket.send(file_name.encode('utf-8'))

                with open(file_path, 'rb') as file:
                    data = file.read(1024)
                    while data:
                        client_socket.send(data)
                        data = file.read(1024)

                print(f'Sending {file_path} to server completed.')
                break  # Break the loop if successful

        except ConnectionRefusedError:
            print("Server is not available. Retrying in 1 second...")
            time.sleep(1)

if __name__ == "__main__":
    folder_to_watch = 'result'
    full_path_to_watch = os.path.join(os.path.dirname(__file__), folder_to_watch)
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, full_path_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
