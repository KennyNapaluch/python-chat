import socket
import threading


# Function to handle receiving messages
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"Error receiving message: {str(e)}")
            break


# Function to handle sending messages
def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))


# Main function to establish connections
def main():
    # Get the user's IP address and port number
    host = input("Enter your IP address: ")
    port = int(input("Enter a port number: "))

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the host and port
        server_socket.bind((host, port))

        # Listen for incoming connections
        server_socket.listen(1)
        print("Waiting for a connection...")

        # Accept the incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address[0]}:{client_address[1]}")

        # Create two threads for sending and receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,))

        # Start the threads
        receive_thread.start()
        send_thread.start()

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
