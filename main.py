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
            break

def send_messages(client_socket, client_address):
    while True:
        try:
            message = client_address.recv(1024).decode('utf-8')
            if not message:
                break
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to {client_address[0]}:{client_address[1]}: {str(e)}")
            break


def main():
    host = '0.0.0.0'
    port = 8888

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print("Waiting for connections...")

        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=receive_messages, args=(client_socket, client_address))
            client_thread.start()

            # Create a send thread for each client
            send_thread = threading.Thread(target=send_messages, args=(client_socket, client_socket))
            send_thread.start()

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
