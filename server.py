import socket


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)

    print("Server listening on http://localhost:8080")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            request = client_socket.recv(1024).decode('utf-8', errors='ignore')
            print("Request:")
            print(request)

            request_lines = request.splitlines()
            if request_lines:
                first_line = request_lines[0]
                parts = first_line.split()
                path = parts[1] if len(parts) > 1 else '/'
            else:
                path = '/'

            file_map = {
                '/': 'index.html',
                '/index.html': 'index.html',
                '/about.html': 'about.html',
                '/contact.html': 'contact.html',
            }

            if path in file_map:
                filename = file_map[path]
                status = 'HTTP/1.0 200 OK\n\n'
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    response = status + html_content
                except FileNotFoundError:
                    response = 'HTTP/1.0 404 NOT FOUND\n\nNOT FOUND'
            else:
                response = 'HTTP/1.0 404 NOT FOUND\n\nNOT FOUND'

            client_socket.sendall(response.encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()


if __name__ == "__main__":
    main()
