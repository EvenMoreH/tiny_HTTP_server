# HTTP Content Types Reference

## Common HTTP Content Types and Their Use Cases

### 1. `text/plain`
- **Use case:** Sending plain text with no formatting
- **Example:** Logs, simple messages, raw text responses
- **Browser behavior:** Displays as plain text

### 2. `text/html`
- **Use case:** Sending HTML documents for web pages
- **Example:** Web pages, HTML email content
- **Browser behavior:** Renders as a web page with formatting

### 3. `application/json`
- **Use case:** Sending structured data in JSON format
- **Example:** REST API responses, configuration data
- **Browser behavior:** Usually displays raw JSON or downloads file

### 4. `application/xml`
- **Use case:** Sending structured data in XML format
- **Example:** SOAP APIs, RSS feeds, configuration files
- **Browser behavior:** May render as formatted XML or download

### 5. `text/css`
- **Use case:** Sending CSS stylesheets
- **Example:** External CSS files linked in HTML
- **Browser behavior:** Applies styles to the current page

### 6. `text/javascript` or `application/javascript`
- **Use case:** Sending JavaScript code
- **Example:** External JS files, dynamic script loading
- **Browser behavior:** Executes the JavaScript code

### 7. Image Types
- `image/png` - PNG images
- `image/jpeg` - JPEG images
- `image/gif` - GIF images
- `image/svg+xml` - SVG vector images
- **Use case:** Sending image files
- **Browser behavior:** Displays the image

### 8. `application/pdf`
- **Use case:** Sending PDF documents
- **Example:** Reports, invoices, documentation
- **Browser behavior:** Opens in PDF viewer or downloads

### 9. `application/octet-stream`
- **Use case:** Sending arbitrary binary data
- **Example:** File downloads where type is unknown, executables
- **Browser behavior:** Usually prompts for download

### 10. `multipart/form-data`
- **Use case:** Sending form data, especially file uploads
- **Example:** HTML form submissions with files
- **Browser behavior:** Used in form processing

### 11. `application/x-www-form-urlencoded`
- **Use case:** Standard form data without files
- **Example:** Simple HTML form submissions
- **Browser behavior:** Default for form submissions

### 12. Audio/Video Types
- `audio/mpeg` - MP3 audio
- `video/mp4` - MP4 video
- `audio/wav` - WAV audio
- **Use case:** Streaming or downloading media files
- **Browser behavior:** Plays in built-in media player

## Important Notes

- **Always set the correct Content-Type** so clients know how to process the response
- **Mislabeling can cause errors** or incorrect rendering
- **Include charset for text types** (e.g., `text/html; charset=utf-8`)
- **Content-Length should match** the actual body size in bytes

## HTTP Response Structure

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1234
Connection: close

<html>...</html>
```

## Examples in Python

```python
def http_response(status="200 OK", content_type="text/plain; charset=utf-8", body=b""):
    head = [
        f"HTTP/1.1 {status}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        "Connection: close",
    ]
    return ("\r\n".join(head) + "\r\n\r\n").encode("utf-8") + body

# Serve HTML
html_body = b"<html><body><h1>Hello</h1></body></html>"
response = http_response("200 OK", "text/html; charset=utf-8", html_body)

# Serve JSON
json_body = b'{"message": "Hello", "status": "ok"}'
response = http_response("200 OK", "application/json; charset=utf-8", json_body)

# Serve plain text
text_body = b"Hello, world!"
response = http_response("200 OK", "text/plain; charset=utf-8", text_body)
```


# HTTP Request Handling

## Understanding the `handle_request` Function

### 1. Function Purpose

```python
def handle_request(req: bytes) -> bytes:
```
- **Purpose:** This function takes a raw HTTP request (as bytes) and returns an HTTP response (also as bytes).
- **Why bytes?** HTTP messages are transmitted over the network as bytes, not strings.

### 2. Parsing the HTTP Request

```python
    try:
        head = req.split(b"\r\n\r\n", 1)[0].decode("utf-8", "replace")
```
- **Splitting:** `req.split(b"\r\n\r\n", 1)` splits the request into two parts: headers and body. The first part (`[0]`) is the headers.
- **Why `\r\n\r\n`?** In HTTP, headers and body are separated by a blank line (two CRLFs).
- **Decoding:** `.decode("utf-8", "replace")` converts bytes to a string, replacing any invalid bytes with a placeholder. This is safer than failing on bad input.

### 3. Extracting the Request Line

```python
        request_line = head.split("\r\n", 1)[0]
```
- **Splitting:** The headers start with a request line (e.g., `GET /index.html HTTP/1.1`). Splitting on the first CRLF gets just this line.

### 4. Getting Method and Path

```python
        method, path, _ = request_line.split(" ", 2)
```
- **Splitting:** The request line is split by spaces:
    - `method` (e.g., `GET`)
    - `path` (e.g., `/index.html`)
    - `_` (the HTTP version, ignored here)
- **Why `_`?** The underscore is a Python convention for unused variables.

### 5. Error Handling

```python
    except Exception:
        return http_response(status="404 Bad Request", body=b"bad request")
```
- **Try/Except:** If anything goes wrong (bad formatting, decoding errors), the function returns a simple HTTP error response.
- **http_response:** This helper builds a valid HTTP response with status `404 Bad Request` and a body saying `"bad request"`.

### 6. Key Concepts

- **HTTP Request Structure:** Requests start with a line like `GET /path HTTP/1.1`, followed by headers, then a blank line, then the body.
- **Bytes vs Strings:** Network data is bytes; you decode to strings for parsing.
- **Error Handling:** Defensive programming is important—never trust network input!
- **Splitting Strings:** `.split()` is a common way to break up structured text.

### 7. Example

Suppose you receive this request:
```
b"GET /hello HTTP/1.1\r\nHost: localhost\r\n\r\n"
```
- After splitting and decoding, `head` is `"GET /hello HTTP/1.1\r\nHost: localhost"`.
- `request_line` is `"GET /hello HTTP/1.1"`.
- Splitting gives `method = "GET"`, `path = "/hello"`, `_ = "HTTP/1.1"`.

**Summary:**
This function is a basic HTTP request parser with error handling. It demonstrates how to safely extract key information from raw network data and respond appropriately if the input is malformed. Understanding how to split and decode bytes, handle exceptions, and follow protocol structure is essential for network programming in Python.

## HTTP Request Routing - Understanding Server Endpoints

### High-Level Context

This code is part of a minimal HTTP server written in Python. Its job is to handle incoming HTTP requests and generate appropriate HTTP responses. The server supports only the GET method and has three main endpoints:

- `/` or `/index.html` (homepage)
- `/api/hello` (API endpoint)
- Any other path (returns 404 Not Found)

### Step-by-Step Explanation

#### 1. Method Not Allowed Handling

```python
if method != "GET":
    return http_response(status="405 Method Not Allowed", body=b"Only GET Method Supported")
```

- **Purpose:** Ensures the server only responds to GET requests.
- **How:** Checks the HTTP method (e.g., GET, POST, PUT) of the incoming request.
- **Why:** This is a security and simplicity measure. By restricting to GET, the server avoids handling other methods that might require additional logic (like POST data parsing).
- **Response:** If the method is not GET, it returns a 405 status code ("Method Not Allowed") with a plain message in the body.

**Gotcha:** If a client tries to POST or PUT, they get a clear error, which is good API hygiene.

#### 2. Homepage Endpoint Handling

```python
if path == "/" or path == "/index.html":
    return http_response(status="200 OK", content_type="text/html; charset=utf-8", body=INDEX)
```

- **Purpose:** Serves the homepage.
- **How:** Checks if the request path is `/` or `/index.html`.
- **Why:** These are conventional paths for a website's main page.
- **Response:** Returns a 200 OK status, sets the content type to HTML, and sends the contents of `INDEX` (presumably a bytes object containing HTML).

**Gotcha:** If `INDEX` is not defined or not bytes, this could raise an error.

#### 3. API Endpoint Handling

```python
if path == "/api/hello":
    data = {"message": "Hello from my Tiny HTTP Server", "ok": True}
    return http_response(
        status="200 OK",
        content_type="application/json; charset=utf-8",
        body=json.dumps(data).encode("utf-8")
    )
```

- **Purpose:** Provides a simple API endpoint.
- **How:** Checks if the path is `/api/hello`.
- **Why:** Demonstrates how to serve JSON data, which is common for APIs.
- **Response:**
    - Creates a Python dictionary with a message and a status.
    - Serializes it to a JSON string using `json.dumps`.
    - Encodes the JSON string to bytes (required for HTTP response bodies).
    - Returns a 200 OK response with the content type set to JSON.

**Gotcha:** Forgetting `.encode("utf-8")` would cause a type error, since the response body must be bytes.

#### 4. Fallback: 404 Not Found

```python
return http_response(status="404 Not Found", body=b"Not Found")
```

- **Purpose:** Handles all other paths.
- **How:** If none of the above conditions match, this line executes.
- **Why:** Ensures the server responds gracefully to unknown paths.
- **Response:** Returns a 404 status with a simple message.

### Final Notes
- **Error Handling:** The code is robust against unsupported methods and unknown paths.
- **Encoding:** Always encodes response bodies to bytes, as required by HTTP.
- **Extending:** To add more endpoints, just add more if path == ... blocks.

# Python Context Managers

## What Problem Do They Solve?
Many resources (files, sockets, database connections, locks) must be cleaned up (closed or released) even if an error happens. Doing this manually with try/finally everywhere is repetitive and error‑prone. A context manager automates: setup → use → cleanup.

## The with Statement Flow
```
with <expression> as <name>:
    # your code (the "block")
```
Step-by-step:
1. Evaluate <expression> → object (must implement __enter__ and __exit__).
2. Call its __enter__(); the return value (if any) is bound to <name>.
3. Run the block.
4. Call its __exit__(exc_type, exc_val, exc_tb):
   - If no exception: all three are None.
   - If exception occurred: they describe it.
   - If __exit__ returns True the exception is suppressed; else it propagates.

## Built-In Example (Files)
```
with open("data.txt", "r", encoding="utf-8") as f:
    text = f.read()
# Here the file is already closed automatically.
```
Without with you would need:
```
f = open("data.txt", "r", encoding="utf-8")
try:
    text = f.read()
finally:
    f.close()
```

## Your Server Example
In `server.py`:
```
with socket.create_server((HOST, PORT), reuse_port=True) as srv:
    pass  # socket is open inside, auto-closed after block
```
The socket object implements the context manager protocol so it closes itself when the block ends.

## Writing a Custom Context Manager (Class Form)
```
class Demo:
    def __enter__(self):
        print("SETUP")
        return "resource"  # becomes the value after 'as'
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("CLEANUP")
        if exc_type:
            print(f"Handled: {exc_val}")
            return True  # swallow the exception (optional)

with Demo() as r:
    print(r)          # prints 'resource'
    # raise ValueError("boom")  # uncomment to see handling
```

Key points:
- __enter__ does setup; return value is optional.
- __exit__ always runs (even if exception in block).
- Only return True if you intentionally suppress the exception.

## Function Style with contextlib
```
from contextlib import contextmanager
import time

@contextmanager
def timer():
    start = time.perf_counter()
    try:
        yield  # hand control to the with-block
    finally:
        dur = time.perf_counter() - start
        print(f"Elapsed: {dur:.4f}s")

with timer():
    sum(range(1_000_000))
```
How it works: Code before yield = setup; code after yield (in finally) = cleanup.

## Common Built-In Context Managers
- `open()` – files
- `socket.socket()` / `socket.create_server()` – network sockets
- `threading.Lock()` – automatically acquire/release (via `with lock:`)
- `contextlib.suppress(ExceptionType, ...)` – ignore specific exceptions
- `contextlib.redirect_stdout()` – temporarily redirect output
- `tempfile.TemporaryDirectory()` – creates & removes a temp folder

## Typical Use Cases
- Resource management (files, sockets, DB connections)
- Locks (avoid forgetting to release)
- Temporary state changes (current directory, environment variables, precision)
- Timing / profiling / logging scopes
- Transactions (commit or rollback)

## Minimal Mental Model
Setup → Work → Cleanup (guaranteed)

## Quick Exercise Ideas
1. Write a context manager that counts how many exceptions occurred inside.
2. Create one that temporarily changes `os.environ["MODE"]` then restores it.
3. Implement one that opens two files at once and yields a tuple.

## Troubleshooting Tips
- If cleanup is not happening: ensure you're actually using `with` and not just calling `__enter__` manually.
- If exceptions vanish unexpectedly: check if `__exit__` returns True unintentionally.
- Avoid heavy work inside `__enter__`; keep it fast.

## Template (Class)
```
class MyCM:
    def __enter__(self):
        # setup
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        # cleanup (always runs)
        # return True to swallow, or False/None to propagate
        return False
```

## Template (Function)
```
from contextlib import contextmanager

@contextmanager
def my_cm():
    # setup
    try:
        yield <value>
    finally:
        # cleanup
        pass
```

# Line-by-line: server accept loop

Below is the exact code from `server.py` that opens the listening socket, accepts client connections, reads an HTTP request, and sends a response. The section that follows explains every line and why it's written that way — useful as a teaching reference.

```python
with socket.create_server((HOST, PORT), reuse_port=True) as server:
    print(f"Serving on http://{HOST}:{PORT}")

    while True:
        connection, address = server.accept()
        with connection:
            buffer = b""
            while b"\r\n\r\n" not in buffer and len(buffer) < 65536:
                chunk = connection.recv(4096)
                if not chunk: break
                buffer += chunk
            connection.sendall(handle_request(buffer))
```

Line-by-line explanation

1) **with socket.create_server((HOST, PORT), reuse_port=True) as server:**
- Calls `socket.create_server(...)`, a convenience factory that returns a bound, listening TCP socket.
- `(HOST, PORT)` is the bind tuple; `reuse_port=True` requests the SO_REUSEPORT option when available.
- Using `with` turns the listening socket into a context manager: when the block exits the socket is closed automatically.
- Why use `with` here? It guarantees the listening socket is closed if the program later exits the block (e.g., on an unhandled exception), reducing resource leaks.

2) **print(f"Serving on http://{HOST}:{PORT}")**
- Prints a human-readable message to stdout so whoever started the server knows it's listening and on which address:port.
- In production you'd typically log this instead of printing.

3) **while True:**
- An infinite loop that repeatedly accepts and handles incoming client connections.
- This server is synchronous and single-threaded: it processes one connection at a time. That keeps the code simple for teaching but limits concurrency.

4) **connection, address = server.accept()**
- `accept()` blocks until a client connects. It returns a tuple `(conn_socket, client_address)`.
- `connection` is a new socket object that represents the connection to that single client; `address` is the client socket address (usually `(ip, port)`).
- Since `accept()` blocks, the server will wait here if there are no incoming connections.

5) **with connection:**
- The accepted connection socket is used as a context manager so it will be closed automatically when the `with` block finishes.
- This ensures cleanup even if an exception occurs while handling the client.

6) **buffer = b""**
- Initialize an empty byte string to collect data read from the client.
- Network I/O deals with bytes, not Python strings, so the buffer is a `bytes` object.

7) **while b"\r\n\r\n" not in buffer and len(buffer) < 65536:**
- This loop collects data until either:
    - the HTTP header terminator (CRLF CRLF) is seen in the buffer, or
    - the buffer reaches 65,536 bytes (64 KiB), which acts as a safety cap to avoid unbounded memory growth.
- The server assumes reading the headers is sufficient for the simple GET handling implemented; it doesn't yet parse or read a request body.

8) **chunk = connection.recv(4096)**
- `recv(4096)` reads up to 4096 bytes from the socket. It may return fewer bytes.
- `recv` blocks until at least one byte is available (unless a timeout is set), or returns `b""` if the peer closed the connection.

9) **if not chunk: break**
- If `recv()` returns an empty bytes object (`b""`), the client closed the connection; break from the read loop to avoid waiting forever.

10) **buffer += chunk**
- Append the newly received bytes to the buffer.
- For small headers this is fine; for many or large chunks building a list and `b"".join(parts)` is more efficient.

11) **connection.sendall(handle_request(buffer))**
- Call `handle_request(buffer)` which:
    - extracts headers from `buffer` (splitting by `b"\r\n\r\n"`),
    - decodes the header portion with `utf-8` using replacement for invalid bytes,
    - parses the request line (method, path, version),
    - checks `method` and `path` and returns a full HTTP response as bytes via `http_response(...)`.
- `sendall(...)` sends the entire response bytes to the client. It blocks until all bytes are transmitted or an error occurs.
- After the `with connection` block finishes, the client socket is closed automatically.

How helper functions tie in (quick mapping)
- `socket.create_server`: returns the listening socket used for `accept()`.
- `accept()`: produces a connected socket for a single client.
- `recv`/`sendall`: socket methods for reading/writing bytes.
- `handle_request`: parses request bytes and returns a full HTTP response (status line, headers, body) as bytes.

Important gotchas and limitations (teaching notes)
- Single-threaded & blocking: only one client is handled at a time; a slow client will block others.
- No request bodies: the read loop only waits for headers (CRLF CRLF). POSTs or requests with bodies (Content-Length or chunked encoding) are not supported.
- No keep-alive: the server sends `Connection: close` and closes the connection after one request/response.
- No timeouts: if a client connects but sends data very slowly (or stops mid-request), the server could block indefinitely. Use `connection.settimeout(...)` to avoid this.
- Buffer growth: concatenating bytes repeatedly can be inefficient for lots of small reads; use a list of chunks and `b"".join(...)` for efficiency.

Small improvement examples (teaching recipes)

- Set a per-connection timeout to avoid hung connections:

```python
connection, address = server.accept()
with connection:
    connection.settimeout(5.0)  # 5-second recv timeout
    buffer = b""
    # ...existing read loop...
```

- Handle each connection in a thread for concurrency:

```python
import threading

def handle_conn(conn, addr):
    with conn:
        conn.settimeout(5.0)
        buffer = b""
        while b"\r\n\r\n" not in buffer and len(buffer) < 65536:
            chunk = conn.recv(4096)
            if not chunk: break
            buffer += chunk
        conn.sendall(handle_request(buffer))

while True:
    conn, addr = server.accept()
    t = threading.Thread(target=handle_conn, args=(conn, addr), daemon=True)
    t.start()
```

- To support request bodies (POST): after parsing headers, check `Content-Length` and read the indicated number of bytes before calling `handle_request`.

Short summary for learners
- This block implements the minimal lifecycle for a simple HTTP server: bind/listen → accept → read request bytes → produce response → send response → close connection. It's intentionally simple so you can see the core socket primitives and how they map to HTTP concepts.
