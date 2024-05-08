# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    print("Accepted peer: ", addr)

    response: str = "HTTP/1.1 200 OK \r\n \r\n".encode()

    conn.send(response)

    print("Connection closed.")



if __name__ == "__main__":
    main()
