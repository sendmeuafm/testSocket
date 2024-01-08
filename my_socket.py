import socket

# server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# server.bind(("127.0.0.1",2000))

class MySocket():
    root_folder="views"
    def start_my_server(self)->None:
        try:
            server = socket.create_server(("127.0.0.1",2000))
            server.listen(4)
            while True:
                client_socket, address = server.accept()
                data = client_socket.recv(1024).decode("utf-8")
                client_socket.send(self.load_page_from_server(data))
                client_socket.shutdown(socket.SHUT_WR)
                print(data)
        except KeyboardInterrupt:
            server.close()

    def load_page_from_server(self,request_data: str):
        return_code='200'


        try:
            path = request_data.split(' ')[1].split('?')[0]
        except:
            path = '/'

        if path.strip() == '/':
            path = '/index.html'

        try:
            file_extension = path.split('.')[-1]
        except:
            file_extension = "html"

        print(f'ext {file_extension}')
        context_type = "text\html"
        # if file_extension == "" or file_extension.find("/") != -1:
        #     file_extension = "html"
        if file_extension == "ico" or file_extension == "png" or file_extension == "jpeg"  or file_extension == "jpg":
            context_type="image/ico"



        with open(f'{self.root_folder}/_top', 'rb') as file:
            toppage = file.read()

        with open(f'{self.root_folder}/_bottom', 'rb') as file:
            bottompage = file.read()

        with open(f'{self.root_folder}/menu', 'rb') as file:
            menupage = file.read()

        try:
            with open(self.root_folder+path, 'rb') as file:
                response=file.read()
        except FileNotFoundError:
            file_extension = "html"
            return_code='404'
            with open(f'{self.root_folder}/nopage.html', 'rb') as file:
                response=file.read()

        HDRS=f'HTTP/1.1 {return_code} OK\r\nContent-Type: {context_type}; charset=utf-8\r\n\r\n'
        if file_extension == "html":
            return HDRS.encode('utf-8')+toppage+menupage+response+bottompage
        else:
            return HDRS.encode('utf-8')+response