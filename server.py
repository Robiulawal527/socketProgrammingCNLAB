import socket


HOST = "127.0.0.1"
PORT = 8080


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server running at http://{HOST}:{PORT}")

    file_map = {
        "/": "index.html",
        "/index.html": "index.html",
        "/about.html": "about.html",
        "/contact.html": "contact.html"
    }

    while True:
        client_socket, client_address = server_socket.accept()

        try:
            request = client_socket.recv(1024).decode(
                "utf-8",
                errors="ignore"
            )

            print("---------------------------------------")
            print("Client:", client_address)
            print(request)

            request_lines = request.splitlines()

            path = "/"

            if request_lines:
                parts = request_lines[0].split()

                if len(parts) >= 2:
                    path = parts[1]

            if path in file_map:

                filename = file_map[path]

                try:
                    with open(filename, "r", encoding="utf-8") as file:
                        html_content = file.read()

                    response = (
                        "HTTP/1.0 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        "\r\n"
                        + html_content
                    )

                except FileNotFoundError:

                    response = (
                        "HTTP/1.0 404 NOT FOUND\r\n"
                        "Content-Type: text/html\r\n"
                        "\r\n"
                        "<h1>404 NOT FOUND</h1>"
                    )

            else:

                response = (
                    "HTTP/1.0 404 NOT FOUND\r\n"
                    "Content-Type: text/html\r\n"
                    "\r\n"
                    "<h1>404 NOT FOUND</h1>"
                )

            client_socket.sendall(response.encode())

        except Exception as e:
            print("Error:", e)

        finally:
            client_socket.close()


if __name__ == "__main__":
    main()