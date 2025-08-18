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

# Creating a socket? :
