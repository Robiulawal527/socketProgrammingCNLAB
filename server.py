import socket

HOST = "127.0.0.1"
PORT = 8080


def build_response(status, body):
    body_bytes = body.encode("utf-8")

    response = (
        f"{status}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("utf-8") + body_bytes

    return response


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    print("Server running:")
    print("http://localhost:8080")
    print("http://127.0.0.1:8080")

    while True:
        client_socket, addr = server_socket.accept()

        try:
            request = client_socket.recv(4096).decode("utf-8", errors="ignore")

            lines = request.splitlines()
            path = "/"

            if lines:
                parts = lines[0].split()
                if len(parts) >= 2:
                    path = parts[1]

            # ignoring fevicon requ
            if path == "/favicon.ico":
                client_socket.close()
                continue

            # printing only real requests (not favicon)
            print("\n--- REQUEST ---")
            print(addr)
            print(path)

            # routing
            if path == "/":
                file_name = "index.html"
            elif path.startswith("/") and path.endswith(".html"):
                file_name = path[1:]
            else:
                file_name = None

            # the  response handling
            if file_name:
                try:
                    with open(file_name, "r", encoding="utf-8") as f:
                        html = f.read()

                    response = build_response("HTTP/1.0 200 OK", html)

                    print("Response:HTTP/1.0 200 OK")

                except FileNotFoundError:
                    response = build_response(
                        "HTTP/1.0 404 NOT FOUND",
                        "<h1>404 NOT FOUND</h1>"
                    )

                    print("Response:HTTP/1.0 404 NOT FOUND")

            else:
                response = build_response(
                    "HTTP/1.0 404 NOT FOUND",
                    "<h1>404 NOT FOUND</h1>"
                )

                print("Response:HTTP/1.0 404 NOT FOUND")

            client_socket.sendall(response)

        except Exception as e:
            print("Error:", e)

        finally:
            client_socket.close()


if __name__ == "__main__":
    main()