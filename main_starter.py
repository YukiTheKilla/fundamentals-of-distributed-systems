import subprocess
import concurrent.futures
import os
import platform
import signal
import sys
import socket

def check_server(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=5):
            print(f"Server {ip}:{port} is responding.")
    except (socket.timeout, socket.error) as e:
        print(f"Error: {e}")
        print(f"Server {ip}:{port} is not responding. Retrying...")

def start_server(server_path):
    try:
        if platform.system().lower() == 'windows':
            subprocess.Popen(["python", server_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(["python", server_path])
    except Exception as e:
        print(f"Error starting server: {e}")

def start_servers(server_paths):
    # Start servers concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(start_server, server_paths)

def signal_handler(sig, frame):
    print("Ctrl+C received. Terminating servers.")
    sys.exit(0)

if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    
    server_paths = [
        os.path.join(base_path, "machine/watcher.py"),
        os.path.join(base_path, "server_1/pinger.py"),
        os.path.join(base_path, "server_1/watcher.py"),
        os.path.join(base_path, "server_2/pinger.py"),
        os.path.join(base_path, "server_2/watcher.py")
        
    ]

    signal.signal(signal.SIGINT, signal_handler)

    start_servers(server_paths)
