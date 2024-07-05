import socket
import threading
import os

def start_server(server_ip, server_port):
    try:
        # Create a socket object for server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the server address
        server_socket.bind((server_ip, server_port))

        # Listen for incoming connections
        server_socket.listen(5)

        print(f"Server is listening on {server_ip}:{server_port}")

        # Accept connections from outside
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established!")

            # Start a new thread to handle client communication
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

    except OSError as e:
        if e.errno == 10048:
            print(f"Error: Port {server_port} is already in use.")
        else:
            print(f"Error occurred: {str(e)}")

    except Exception as e:
        print(f"Unexpected error in server: {str(e)}")

def handle_client(client_socket):
    try:
        while True:
            # Receive client data
            client_data = client_socket.recv(1024).decode("utf-8")

            if not client_data:
                break

            print(f"Received from client: {client_data}")

            # Example: Send a response back to the client
            client_socket.send(bytes("Message received!", "utf-8"))

    except Exception as e:
        print(f"Error handling client: {str(e)}")

    finally:
        # Close the client socket
        client_socket.close()

def start_client(server_ip, server_port):
    try:
        # Create a socket object for client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((server_ip, server_port))

        print(f"Connected to server {server_ip}:{server_port}")

        # Example: Send data to server
        message = "Hello from client!"
        client_socket.send(bytes(message, "utf-8"))

        # Receive response from server
        server_response = client_socket.recv(1024).decode("utf-8")
        print(f"Server response: {server_response}")

    except OSError as e:
        if e.errno == 10061:
            print(f"Error: Connection refused. Make sure the server is running on {server_ip}:{server_port}.")
        else:
            print(f"OSError connecting to server: {str(e)}")

    except Exception as e:
        print(f"Unexpected error in client: {str(e)}")

    finally:
        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    try:
        # Attempt to run the server
        server_ip = input("Enter the server IP address to bind (use 0.0.0.0 for all interfaces): ")
        server_port = int(input("Enter the server port number to bind: "))

        # Check if rat_server.py exists
        if not os.path.exists("rat_server.py"):
            raise FileNotFoundError("File 'rat_server.py' not found.")

        # Start server in a separate thread
        server_thread = threading.Thread(target=start_server, args=(server_ip, server_port))
        server_thread.start()

        # Client configuration (for testing, you can modify or remove this part)
        client_ip = input("Enter the server IP address to connect to: ")
        client_port = int(input("Enter the server port number to connect to: "))

        # Start client in the main thread
        start_client(client_ip, client_port)

    except FileNotFoundError as e:
        print(f"FileNotFoundError: {str(e)}")

    except ValueError:
        print("Error: Please enter a valid port number.")

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

    except Exception as e:
        print(f"Unexpected error: {str(e)}")