import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55556

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024) # recieve message
            broadcast(message) # broadcasting it to all
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nicknames = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def recieve():
    while True:
        # Accept Connection
        client, address = server.accept() # Accept client when they connect
        print(f"Connected with {str(address)}")

        # Request And Store Nickname
        client.send('NICK'.encode('ascii')) # Send Nick to client, so let him know
        nickname = client.recv(1024).decode('ascii') # recieve nickname
        nicknames.append(nickname)
        clients.append(client) # add to list

        # Print And Broadcast Nickname
        print(f"Nickname pf the clients is {nickname}!")
        broadcast(f'{nickname} joined the chat!'.encode(('ascii'))) 
        client.send('Connected to the server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,)) 
        thread.start()

print('server is listing...')
recieve()
