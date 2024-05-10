# implemented by @NickPhilomath
# thanks for Codecrafters.io for creating masterpiece learning platform.

import socket

BUFFER_SIZE = 1024


# views to handle requests
def home(request) -> str:
    response = "HTTP/1.1 200 OK \r\n\r\n".encode()
    return response

def handle404(request) -> str:
    response = "HTTP/1.1 404 Not Found \r\n\r\n".encode()
    return response


class Path:
    def __init__(self, url, view) -> None:
        self.url = url
        self.view = view


urlpatterns = [
    Path('/', home),
]

# this function returns specific function that 
# is responsible to handle given url
def get_url_view(url):
    for path in urlpatterns:
        if path.url == url:
            return path.view
        
    return handle404


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    print("Accepted peer: ", addr)

    request = conn.recv(BUFFER_SIZE).decode()

    start_line = request.split('\r\n')[0]

    req_url = start_line.split(' ')[1]

    print('request url: ', req_url)

    view = get_url_view(req_url)

    response  = view(request)

    conn.send(response)

    print("Connection closed.")



if __name__ == "__main__":
    main()
