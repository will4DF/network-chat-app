import socket
import threading

HOST = "127.0.0.1"
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

print(f"Server running on {HOST}:{PORT}")

def broadcast(message, sender_client=None):
    for client in clients:
        if client != sender_client:
            try:
                client.send(message.encode())
            except:
                pass

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode()

            # Client disconnected unexpectedly
            if not message:
                break

            broadcast(message, sender_client=client)

        except:
            break

    # Clean up when disconnected
    index = clients.index(client)
    username = usernames[index]

    clients.remove(client)
    usernames.remove(username)

    client.close()
    broadcast(f"⚠️ {username} has disconnected.")
    print(f"{username} disconnected.")

def receive_connections():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("USERNAME".encode())
        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        print(f"{username} joined the chat.")
        broadcast(f"🎉 {username} joined the chat!")

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
