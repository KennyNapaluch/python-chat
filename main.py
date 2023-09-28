import socket
import threading

# Create a socket object
socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific host and port
host = '127.0.0.1'  # Listen on localhost
port = 8889
socket_instance.bind((host, port))

# Maintain a list of connected peers
peers = []


# Function to send messages to all connected peers
def broadcast(message, sending_peer):
    for peer in peers:
        if peer != sending_peer:
            try:
                peer.send(message)
            except:
                # Remove the peer if there's an issue with the connection
                remove_peer(peer)


# Function to remove a peer from the list
def remove_peer(peer):
    if peer in peers:
        peers.remove(peer)


# Function to handle individual peer connections
def handle_peer(peer):
    while True:
        try:
            message = peer.recv(1024)
            if not message:
                remove_peer(peer)
                break
            broadcast(message, peer)
        except:
            remove_peer(peer)
            break


# Start listening for incoming connections
socket_instance.listen()

print(f"Server is listening on {host}:{port}")


# Function to accept incoming peer connections
def accept_peers():
    while True:
        peer, peer_address = socket_instance.accept()
        peers.append(peer)
        print(f"Connection established with {peer_address}")

        # Create a thread to handle the peer
        peer_thread = threading.Thread(target=lambda: handle_peer(peer))
        peer_thread.start()


# Start accepting peer connections in a separate thread
accept_thread = threading.Thread(target=accept_peers)
accept_thread.start()

# Main loop for sending messages
while True:
    message = input()
    broadcast(message.encode('utf-8'), None)  # Set sending_peer to None for messages from the server
