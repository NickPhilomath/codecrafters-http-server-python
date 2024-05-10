# implemented by @NickPhilomath
# thanks for Codecrafters.io for creating masterpiece learning platform.

import socket

PORT_NUMBER = 4221
BUFFER_SIZE = 1024


# views to handle requests
def home(request) -> str:
    response = "HTTP/1.1 200 OK \r\n\r\n".encode()
    return response

def hello(request) -> str:
    response = "HTTP/1.1 200 OK \r\n\r\n hello world".encode()
    return response

def handle404(request) -> str:
    response = "HTTP/1.1 404 Not Found \r\n\r\n".encode()
    return response


class Request:
    def __init__(self) -> None:
        pass


class Path:
    def __init__(self, url, view) -> None:
        self.url = url
        self.view = view


urlpatterns = [
    Path('/', home),
    Path('/hello', hello),
]

# this function returns specific function that 
# is responsible to handle given url
def get_url_view(url):
    for path in urlpatterns:
        if path.url == url:
            return path.view
        
    return handle404


def handle_server_request(request):
    start_line, headers, body, *other = request.split('\r\n')

    method, req_url, http_version, *other = start_line.split(' ')

    # print(start_line, headers, body, other, sep=" ### ")
    # print(method, url, http_v, sep=" ### ")

    view = get_url_view(req_url)
    response = view(request)
    return response


def main():
    print(f"started server at port {PORT_NUMBER}.")

    server_socket = socket.create_server(("localhost", PORT_NUMBER), reuse_port=True)

    conn, addr = server_socket.accept() # wait for client
    print("Accepted peer: ", addr)

    request = conn.recv(BUFFER_SIZE).decode()
    response = handle_server_request(request)
    conn.send(response)

    print("Connection closed.")



if __name__ == "__main__":
    main()
