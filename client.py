
import socket
import threading

HOST = "127.0.0.1"
PORT = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter your username: ")

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()

            # Server asks for username
            if message == "USERNAME":
                client.send(username.encode())
            else:
                print(message)

        except:
            print("⚠️ You have been disconnected from the server.")
            client.close()
            break

def send_messages():
    while True:
        message = input("")

        # User types /quit → disconnect and exit cleanly
        if message.lower() == "/quit":
            client.send(f"⚠️ {username} has left the chat.".encode())
            client.close()
            print("You disconnected.")
            break

        full_message = f"{username}: {message}"
        client.send(full_message.encode())

# Threads so you can send + receive at the same time
threading.Thread(target=receive_messages).start()
threading.Thread(target=send_messages).start()