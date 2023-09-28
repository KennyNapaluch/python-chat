import socket
import threading


def receive_messages(client_socket, client_address):
    print(f"Connected to {client_address[0]}:{client_address[1]}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(f"{client_address[0]}:{client_address[1]} says: {message}")
        except Exception as e:
            print(f"Error receiving message from {client_address[0]}:{client_address[1]}: {str(e)}")
            break


def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))


def main():
    host = '0.0.0.0'
    port = 8888

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print("Waiting for a connection...")

        client_socket, client_address = server_socket.accept()

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, client_address))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))

        receive_thread.start()
        send_thread.start()

        # Now, we allow the user to initiate a connection to the other peer
        while True:
            target_port = 8888

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                client_socket.connect((client_address[0], target_port))
                print(f"Connected to {client_address[0]}:{target_port}")
                send_thread = threading.Thread(target=send_messages, args=(client_socket,))
                send_thread.start()
                break
            except Exception as e:
                print(f"Connection failed: {str(e)}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
