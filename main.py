import socket
import threading

# Create a lock for output synchronization
output_lock = threading.Lock()

# Define user information
adrianna_ip = '192.168.4.62'
kenny_ip = '192.168.4.21'
my_ip = socket.gethostbyname(socket.gethostname())
if my_ip == kenny_ip:
    me = 'Kenny'
    you = 'Adrianna'
elif my_ip == adrianna_ip:
    me = 'Adrianna'
    you = 'Kenny'
port = 8888


def safe_print(message):
    # Lock to ensure only one thread prints at a time
    with output_lock:
        print(message)


def receive_messages(client_socket, client_address):
    safe_print(f"Connected to {you}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            safe_print(f"{you} says: {message}")
        except Exception as e:
            safe_print(f"Error receiving message from {client_address[0]}:{client_address[1]}: {str(e)}")
            client_socket.close()
            break


def send_messages(client_socket, client_address):
    while True:
        try:
            message = input()  # Input message from the server user
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            safe_print(f"Error sending message to {client_address[0]}:{client_address[1]}: {str(e)}")
            client_socket.close()
            break


def server_thread():
    host = '0.0.0.0'
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        safe_print("Waiting for connections...")
        while True:
            client_socket, client_address = server_socket.accept()
            safe_print(f"Connected to {you} @ {client_address[0]}:{client_address[1]}")
            # Start a thread to receive messages from the client
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_address))
            receive_thread.start()
            # Start a thread to send messages to the client
            send_thread = threading.Thread(target=send_messages, args=(client_socket, client_address))
            send_thread.start()
    except Exception as e:
        safe_print(f"Error: {str(e)}")


def client_thread(remote_host, remote_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((remote_host, remote_port))
        safe_print(f"Connected to {remote_host}:{remote_port}")
        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, (remote_host, remote_port)))
        receive_thread.start()
        # Start a thread to send messages to the server
        send_thread = threading.Thread(target=send_messages, args=(client_socket, (remote_host, remote_port)))
        send_thread.start()
    except Exception as e:
        safe_print(f"Error connecting to {you} @ {remote_host}:{remote_port}: {str(e)}")


def main():
    print("1. Start as server")
    print("2. Connect to a server")
    choice = input("Enter your choice (1/2): ")
    if choice == '1':
        server_thread()
    elif choice == '2':
        if me == 'Kenny':
            client_thread(adrianna_ip, port)
        elif me == 'Adrianna':
            client_thread(kenny_ip, port)
    else:
        safe_print("Invalid choice. Please enter '1' or '2'.")


if __name__ == "__main__":
    main()
