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
            print(f"OSError occurred: {str(e)}")

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

if __name__ == "__main__":
    try:
        # Attempt to run the server
        server_ip = input("Enter the server IP address to bind (use 0.0.0.0 for all interfaces): ")
        server_port = int(input("Enter the server port number to bind: "))

        # Start server in a separate thread
        server_thread = threading.Thread(target=start_server, args=(server_ip, server_port))
        server_thread.start()

        # Keep the main thread running to handle user input or other tasks
        while True:
            pass  # Replace with actual main thread tasks as needed

    except ValueError:
        print("Error: Please enter a valid port number.")

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

    except Exception as e:
        print(f"Unexpected error: {str(e)}")