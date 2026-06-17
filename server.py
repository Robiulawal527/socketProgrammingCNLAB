import socket

def main():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to localhost port 8080
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    
    print("Server listening on http://localhost:8080")
    
    while True:
        # Accept connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        
        try:
            # Receive request
            request = client_socket.recv(1024).decode('utf-8')
            print("Request:")
            print(request)
            
            # Parse the request to get the path
            request_lines = request.split('\r\n')
            if request_lines:
                first_line = request_lines[0]
                parts = first_line.split()
                if len(parts) > 1:
                    path = parts[1]
                else:
                    path = '/'
            else:
                path = '/'
            
            # Determine the file to serve
            if path == '/' or path == '/index.html':
                filename = 'index.html'
                status = 'HTTP/1.0 200 OK\r\n\r\n'
            elif path == '/about.html':
                filename = 'about.html'
                status = 'HTTP/1.0 200 OK\r\n\r\n'
            elif path == '/contact.html':
                filename = 'contact.html'
                status = 'HTTP/1.0 200 OK\r\n\r\n'
            else:
                # 404
                response = 'HTTP/1.0 404 NOT FOUND\r\n\r\n'
                client_socket.sendall(response.encode('utf-8'))
                client_socket.close()
                continue
            
            # Read the HTML file
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Send response
                response = status + html_content
                client_socket.sendall(response.encode('utf-8'))
            except FileNotFoundError:
                # Fallback 404 if file missing
                response = 'HTTP/1.0 404 NOT FOUND\r\n\r\n'
                client_socket.sendall(response.encode('utf-8'))
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
