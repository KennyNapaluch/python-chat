import socket
import threading

def receive_messages(client_socket, client_address):
    print(f"Connected to {client_address[0]}:{client_address[1]}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{client_address[0]}:{client_address[1]} says: {message}")
        except Exception as e:
            print(f"Error receiving message from {client_address[0]}:{client_address[1]}: {str(e)}")
            client_socket.close()
            break

def send_messages(client_socket, client_address):
    while True:
        try:
            message = input("You: ")  # Input message from the server user
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to {client_address[0]}:{client_address[1]}: {str(e)}")
            client_socket.close()
            break

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")
        # Start a thread to receive messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, (host, port)))
        receive_thread.start()
        # Start a thread to send messages to the server
        send_thread = threading.Thread(target=send_messages, args=(client_socket, (host, port)))
        send_thread.start()
    except Exception as e:
        print(f"Error connecting to {host}:{port}: {str(e)}")

def main():
    while True:
        print("1. Start as server")
        print("2. Connect to a server")
        choice = input("Enter your choice (1/2): ")
        if choice == '1':
            host = '0.0.0.0'
            port = 8888
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                server_socket.bind((host, port))
                server_socket.listen(5)
                print("Waiting for connections...")
                while True:
                    client_socket, client_address = server_socket.accept()
                    print(f"Connected to {client_address[0]}:{client_address[1]}")
                    # Start a thread to receive messages from the client
                    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_address))
                    receive_thread.start()
                    # Start a thread to send messages to the client
                    send_thread = threading.Thread(target=send_messages, args=(client_socket, client_address))
                    send_thread.start()
            except Exception as e:
                print(f"Error: {str(e)}")
        elif choice == '2':
            remote_host = input("Enter the remote server's IP address: ")
            remote_port = int(input("Enter the remote server's port: "))
            connect_to_server(remote_host, remote_port)
        else:
            print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    main()
