import socket

HOST = "localhost"
PORT = 8080


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server running at http://{HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()

        try:
            request = client_socket.recv(1024).decode(
                "utf-8",
                errors="ignore"
            )

            print("--------------------------------")
            print("Client:", client_address)
            print(request)

            path = "/"

            request_lines = request.splitlines()

            if request_lines:
                parts = request_lines[0].split()

                if len(parts) >= 2:
                    path = parts[1]

            # Routing
            if path == "/":
                filename = "index.html"

            elif path.startswith("/") and path.endswith(".html"):
                filename = path[1:]

            else:
                filename = None

            # Serve file
            if filename:
                try:
                    with open(filename, "r", encoding="utf-8") as file:
                        html_content = file.read()

                    response = (
                        "HTTP/1.0 200 OK\n\n"
                        + html_content
                    )

                except FileNotFoundError:
                    response = (
                        "HTTP/1.0 404 NOT FOUND\n\n"
                        "<h1>404 Not Found</h1>"
                    )

            else:
                response = (
                    "HTTP/1.0 404 NOT FOUND\n\n"
                    "<h1>404 Not Found</h1>"
                )

            client_socket.sendall(response.encode("utf-8"))

        except Exception as e:
            print("Error:", e)

        finally:
            client_socket.close()


if __name__ == "__main__":
    main()