import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Connected to {client_address[0]}:{client_address[1]}")

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{client_address[0]}:{client_address[1]} says: {message}")

    except Exception as e:
        print(f"Error receiving message from {client_address[0]}:{client_address[1]}: {str(e)}")

    finally:
        print(f"Connection to {client_address[0]}:{client_address[1]} closed.")
        client_socket.close()

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
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
