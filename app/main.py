# implemented by @NickPhilomath
# thanks for Codecrafters.io for creating masterpiece learning platform.

import socket

PORT_NUMBER = 4221
BUFFER_SIZE = 1024


class Path:
    def __init__(self, url, view) -> None:
        self.url = url
        self.view = view

    def check_match(self, url):
        pu_list = self.url.split('/') # path urls list
        ru_list = url.split('/') # request urls list

        # check if urls sections are equal
        if len(pu_list) != len(ru_list):
            return {}, False

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
    

class Request:
    def __init__(self, request_raw) -> None:
        head, body, *_ = request_raw.split('\r\n\r\n')
        head_lines = head.split('\r\n')
        # get the first line, others are request headers
        start_line = head_lines.pop(0)
        method, req_url, http_version = start_line.split(' ')

        headers_dic = {}
        # prepare headers
        for header in head_lines:
            header_name, header_value = header.split(": ")
            headers_dic[header_name] = header_value

        self.method = method
        self.url = req_url
        self.headers = headers_dic


class Response:
    headers = {
        "Content-Type": "text/plain",
        "Content-Length": 0
    }
    def __init__(self, data = "", status = 200):
        self.data = data
        self.status = status

    def make_raw(self) -> str:
        # headers = "Content-Type: text/plain\r\n" + f"Content-Length: {msg_length}\r\n"
        # f"HTTP/1.1 200 OK\r\n{headers}\r\n{msg}".encode()

        self.headers["Content-Length"] = len(self.data)

        headers_raw = ""
        for h_key, h_value in self.headers.items():
            headers_raw += f"{h_key}: {h_value}\r\n"

        return f"HTTP/1.1 {self.status} OK\r\n{headers_raw}\r\n{self.data}".encode()


# views to handle requests
def home(request: Request) -> Response:
    return Response(status=200)

def hello(request: Request) -> Response:
    data = "hello world"
    return Response(data, status=200)

def echo(request, url_vars_dic):
    msg = url_vars_dic.get('msg', '')
    msg_length = len(msg)
    return Response(msg, status=200)

def handle404(request) -> str:
    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    return response


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


def handle_server_request(request_raw):
    request = Request(request_raw)
    view = get_url_view(request.url)
    response = view(request)
    return response.make_raw()


def main():
    print(f"started server at port {PORT_NUMBER}.")

    server_socket = socket.create_server(("localhost", PORT_NUMBER), reuse_port=True)

    while True:
        try:
            conn, addr = server_socket.accept() # wait for client
            print("Accepted peer: ", addr)

            request_raw = conn.recv(BUFFER_SIZE).decode()
            response = handle_server_request(request_raw)
            conn.send(response)
        
        except KeyboardInterrupt:
            print("\nStopping server...")
            server_socket.close()
            break



if __name__ == "__main__":
    main()
