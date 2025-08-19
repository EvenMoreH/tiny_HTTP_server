import socket
import json
from pathlib import Path

HOST = "0.0.0.0"
PORT = 5073
# content is required to be send over in bytes
INDEX = Path("index.html").read_bytes()

# http response builder
def http_response(status="200 OK", content_type="text/plain; charset=utf-8", body=b""):
    """
    Constructs an HTTP response message.
    Args:
        status (str): The HTTP status line (default "200 OK").
        content_type (str): The value for the Content-Type header (default "text/plain; charset=utf-8").
        body (bytes): The response body as bytes (default empty).
    Returns:
        bytes: The complete HTTP response message, including headers and body.
    Line-by-line explanation:
        1. The function defines default arguments for status, content_type, and body to allow easy creation of standard responses.
        2. The 'head' list is constructed to hold the HTTP response headers:
            - The first line sets the HTTP version and status code.
            - The second line specifies the content type of the response.
            - The third line sets the content length, calculated from the length of the body in bytes.
            - The fourth line indicates that the connection will be closed after the response.
        3. The headers are joined with CRLF ("\r\n") to comply with HTTP protocol formatting.
        4. Two additional CRLFs are added to separate headers from the body.
        5. The headers are encoded to bytes and concatenated with the body, forming the complete HTTP response.
    """

    head = [
        f"HTTP/1.1 {status}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        "Connection: close",
    ]

    return ("\r\n".join(head) + "\r\n\r\n").encode("utf-8") + body

# function to handle this servers requests including homepage and demo api call
def handle_request(req: bytes) -> bytes:
    """
    Handles an incoming HTTP request and returns an appropriate HTTP response.
    This function processes a raw HTTP request in bytes, parses the request line,
    and determines the correct response based on the HTTP method and requested path.
    Line-by-line explanation:
    1. Attempts to parse the HTTP request:
        - Splits the request into headers and body using the double CRLF delimiter (`\r\n\r\n`).
        - Decodes the header portion from bytes to a UTF-8 string, replacing invalid characters.
        - Extracts the request line (the first line of the header).
        - Splits the request line into HTTP method, path, and protocol version.
    2. If parsing fails at any point, returns a "400 Bad Request" response.
    3. Checks if the HTTP method is "GET":
        - If not, returns a "405 Method Not Allowed" response indicating only GET is supported.
    4. Handles requests for the homepage:
        - If the path is "/" or "/index.html", returns a "200 OK" response with the homepage HTML content.
    5. Handles the "/api/hello" endpoint:
        - If the path is "/api/hello", returns a "200 OK" response with a JSON payload containing a greeting message.
    6. For any other path not explicitly handled:
        - Returns a "404 Not Found" response indicating the resource does not exist.
    Args:
         req (bytes): The raw HTTP request received from the client.
    Returns:
         bytes: The raw HTTP response to be sent back to the client.
    """
    try:
        head = req.split(b"\r\n\r\n", 1)[0].decode("utf-8", "replace")
        request_line = head.split("\r\n", 1)[0]
        method, path, _ = request_line.split(" ", 2)
    except Exception:
        return http_response(status="400 Bad Request", body=b"bad request")

    # method not allowed handling:
    if method != "GET":
        return http_response(status="405 Method Not Allowed", body=b"Only GET Method Supported")

    # homepage endpoint handling
    if path == "/" or path == "/index.html":
        return http_response(status="200 OK", content_type="text/html; charset=utf-8", body=INDEX)

    # api endpoint handling
    if path == "/api/hello":
        data = {"message": "Hello from my Tiny HTTP Server", "ok": True}
        return http_response(status="200 OK", content_type="application/json; charset=utf-8", body=json.dumps(data).encode("utf-8"))

    # handling for all other paths that were not specified
    return http_response(status="404 Not Found", body=b"Not Found")


# Creating a socket and handling incoming connections:
# This section sets up the HTTP server socket and handles incoming client connections in a loop.
#
# Step-by-step explanation:
# 1. Socket creation with error handling:
#    - Attempts to create a server socket with reuse_port=True for better performance
#    - Falls back to basic socket creation if reuse_port is not supported on the platform
#    - Binds to the specified HOST and PORT (0.0.0.0:5073)
#
# 2. Server main loop setup:
#    - Uses context manager (with statement) to ensure proper socket cleanup
#    - Prints server startup message with the listening address
#    - Enters infinite loop to continuously accept new connections
#
# 3. Connection handling for each client:
#    - Accepts incoming connection and gets client address information
#    - Logs each new connection with connection object and client address
#    - Uses context manager for automatic connection cleanup
#
# 4. Request processing with timeout and buffering:
#    - Sets 5-second timeout to prevent hanging connections
#    - Implements buffering system to read complete HTTP requests:
#      * Reads data in 4096-byte chunks
#      * Continues until finding HTTP header delimiter (\r\n\r\n) or reaching 64KB limit
#      * Prevents incomplete request processing and memory exhaustion
#    - Sends the complete buffered request to handle_request() function
#    - Sends the generated HTTP response back to the client
#
# 5. Error handling for various connection issues:
#    - socket.timeout: Handles connections that don't send data within timeout period
#    - ConnectionAbortedError: Handles cases where client forcibly closes connection
#    - General Exception: Catches any other unexpected errors during request processing
#    - All errors are logged with descriptive messages for debugging purposes

try:
    server = socket.create_server((HOST, PORT), reuse_port=True)
except (ValueError, OSError) as e:
    print(f"reuse_port not available on this platform, falling back {e}")
    server = socket.create_server((HOST, PORT))

with server:
    print(f"Serving on http://{HOST}:{PORT}")

    while True:
        connection, address = server.accept()
        print(f"Incoming connection: {connection} // {address}")
        with connection:
            connection.settimeout(5)
            try:
                buffer = b""
                while b"\r\n\r\n" not in buffer and len(buffer) < 65536:
                    chunk = connection.recv(4096)
                    if not chunk: break
                    buffer += chunk
                connection.sendall(handle_request(buffer))
            except socket.timeout:
                print(f"Connection timed out for {address}")
            except ConnectionAbortedError as e:
                print(f"Connection aborted: {e}")
            except Exception as e:
                print(f"Error handling request: {e}")