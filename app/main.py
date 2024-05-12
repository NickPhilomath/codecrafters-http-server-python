# implemented by @NickPhilomath
# thanks for Codecrafters.io for creating masterpiece learning platform.

import socket

PORT_NUMBER = 4221
BUFFER_SIZE = 1024


# views to handle requests
def home(request) -> str:
    response = "HTTP/1.1 200 OK\r\n\r\n".encode()
    return response

def hello(request) -> str:
    response = "HTTP/1.1 200 OK\r\n\r\nhello world".encode()
    return response

def echo(request, url_vars_dic):
    msg = url_vars_dic.get('msg', '')
    msg_length = len(msg)

    headers = "Content-Type: text/plain\r\n" + f"Content-Length: {msg_length}\r\n"

    return f"HTTP/1.1 200 OK\r\n{headers}{msg}".encode()

def handle404(request) -> str:
    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    return response


class Request:
    def __init__(self) -> None:
        pass


class Path:
    def __init__(self, url, view) -> None:
        self.url = url
        self.view = view

    def check_match(self, url):
        pu_list = self.url.split('/') # path urls list
        ru_list = url.split('/') # request urls list

        url_vars_dic = {}  # we store url variable values here and later pass it to view

        for i in range(len(pu_list)):
            if ':' in pu_list[i]: # if url is varialble
                url_varname = pu_list[i]
                url_varname = url_varname[1:] # remove first character colon
                url_vars_dic[url_varname] = ru_list[i]
                continue
            elif pu_list[i] == ru_list[i]:
                continue
            else:
                return {}, False
            
        return url_vars_dic, True


urlpatterns = [
    Path('/', home),
    Path('/hello', hello),
    Path('/echo/:msg', echo),
]

# this function returns specific function that 
# is responsible to handle given url
def get_url_view(url):
    for path in urlpatterns:
        url_vars_dic, path_is_match = path.check_match(url)
        if path_is_match:
            if len(url_vars_dic) == 0:
                return path.view
            else:
                return lambda request: path.view(request, url_vars_dic)
        
    return handle404


def handle_server_request(request):
    start_line, headers, body, *other = request.split('\r\n')
    method, req_url, http_version, *other = start_line.split(' ')

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
