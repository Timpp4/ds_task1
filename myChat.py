import socket 
import threading
import sys

class Server:
        # Create socket that uses IPv4 and TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # List for the connected clients
        connections = []
        
        def __init__(self):
                # Start the server
                self.sock.bind(('127.0.0.1', 10000))
                self.sock.listen(1)
                print("Started the chat server.")

        # Accept connections
        def run(self):
                while True:
                        c, a = self.sock.accept()
                        
                        # Start a thread for the client
                        cThread = threading.Thread(target=self.handler, args=(c, a))
                        cThread.daemon = True
                        cThread.start()
                        
                        # Save client info to list
                        self.connections.append(c)
                        
                        # Print client ip:port
                        print(str(a[0] + ':' + str(a[1]) + " connected."))

        # Recieve message and broadcast it to all connected client
        def handler(self, c, a):
                try:
                        while True:
                                # Recieve message
                                data = c.recv(1024)
                                # Client info broadcast
                                user = str.encode((str(a[0] + ':' + str(a[1]) + " said: ")))
                                data = user + data
                                # Loop connections
                                for connection in self.connections:
                                        # Includes IP:PORT and message
                                        connection.send(data)
                # User disconnected
                except ConnectionResetError:
                                print(str(a[0] + ':' + str(a[1]) + " disconnected."))
                                self.connections.remove(c)
                                c.close()

                        



class Client:
        # Create socket that uses IPv4 and TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def __init__(self, address):
                # Connect to server
                self.sock.connect((address, 10000))
                # Can't recieve and send messages at the same time -> threading
                iThread = threading.Thread(target=self.send)
                iThread.daemon = True
                iThread.start()

                # Recieve messages
                while True:
                        data = self.sock.recv(1024)
                        if not data:
                                break
                        print(str(data, 'utf-8'))

        # Send messages
        def send(self):
                while True:
                        message = input("")
                        if (message != ""):
                                self.sock.send(bytes(message, "utf-8"))
                        else:
                                print("Message can't be empty!")

# User gave an IP address
if (len(sys.argv) > 1):
        print("Type your message and hit enter!")
        print("To disconnect just close the program.")
        client = Client(sys.argv[1])

# Just start the server
else:
        try:
                server = Server()
                server.run()
        except OSError:
                print("Server already running!")
