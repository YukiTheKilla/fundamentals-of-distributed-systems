import socket
import subprocess
import concurrent.futures
import time
import platform
import os

def start_server(server_path):
    try:
        if platform.system().lower() == 'windows':
            subprocess.Popen(["python", server_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(["python", server_path])
    except Exception as e:
        print(f"Error starting server: {e}")

def check_and_launch(server):
    ip, port, alternative_paths = server["ip"], server["port"], server["alternative_paths"]
    try:
        with socket.create_connection((ip, port), timeout=5):
            print(f"Server {ip}:{port} is responding.")
            return True  # Indicate that the server is responding
    except (socket.timeout, socket.error) as e:
        print(f"Error: {e}")
        print(f"Server {ip}:{port} is not responding. Launching alternate scripts asynchronously...")

        # Launch the alternate scripts asynchronously
        for path in alternative_paths:
            start_server(path)

        return True
    
if __name__ == "__main__":
    servers = [
        {"ip": "127.0.0.1", "port": 1111, "alternative_paths": [os.path.join(os.path.dirname(__file__), "collector_port.py")]},
        {"ip": "127.0.0.1", "port": 2222, "alternative_paths": [os.path.join(os.path.dirname(__file__), "filename_scout_port.py")]},
        {"ip": "127.0.0.1", "port": 3333, "alternative_paths": [os.path.join(os.path.dirname(__file__), "shipment_port.py")]},
        {"ip": "127.0.0.1", "port": 222, "alternative_paths": [os.path.join(os.path.dirname(__file__), "catcher_port.py")]},
    ]

    while servers:  # Continue monitoring as long as there are servers in the list
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(check_and_launch, server) for server in servers]

            # Wait for all threads to complete
            concurrent.futures.wait(futures)

        time.sleep(5)

