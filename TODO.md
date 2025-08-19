# Project skeleton

- [x] Create a folder (e.g., tiny-http/).
- [x] Add server.py for the Python code.
- [x] Add an index.html file (any valid HTML).
- [x] Ensure Python 3.8+ is installed (python3 --version).

# Basic config

- [x] Decide bind address/port (e.g., HOST="0.0.0.0", PORT=8080).
- [x] Understand that 0.0.0.0 exposes to your LAN; use 127.0.0.1 for local only.
- [x] Make sure port 8080 is free (change if needed).

# Load static content

- [x] Read your landing page once at startup: INDEX = Path("index.html").read_bytes().
- [x] Keep it as bytes to avoid encoding surprises.

# HTTP response builder

- [x] Implement a helper that creates the raw HTTP response:
- [x] Status line: HTTP/1.1 200 OK (or other).
- [x] Mandatory headers: Content-Type, Content-Length, Connection: close.
- [x] Blank line \r\n\r\n, then the body (bytes).
- [x] Compute Content-Length from the byte length, not chars.

# Request reading (from socket)

- [x] Accept a TCP connection and read until the end of headers \r\n\r\n.
- [x] Impose a max header size (e.g., 64 KiB) to avoid abuse.
- [x] Don't assume the whole request arrives in one recv; loop until done or limit hit.
- [x] If the peer closes early, handle gracefully.

# Request parsing (minimal)

- [x] Split the request into headers/body at \r\n\r\n.
- [x] Decode headers as UTF-8 with "replace" on errors.
- [x] Extract the request line (first line) and split into method, path, http-version.
- [x] On failure, return 400 Bad Request.

# Method gating

- [x] Allow only GET for this tiny server.
- [x] For anything else, return 405 Method Not Allowed (optionally include Allow: GET).

# Simple routing

- [x] If path is / or /index.html: return the HTML you preloaded with Content-Type: text/html; charset=utf-8.
- [x] If path is /api/hello:
    - [x] Build a small dict payload.
    - [x] json.dumps(...) then .encode("utf-8").
    - [x] Use Content-Type: application/json; charset=utf-8.
- [x] Anything else → 404 Not Found.

# Socket server loop

- [x] Create a listening socket: socket.create_server((HOST, PORT), reuse_port=True).
- [x] Print the URL for convenience.
- [x] In a while True loop: accept(), read headers, sendall(handle_request(buf)), close.
- [x] Wrap connection handling in a context manager (with conn:) so it always closes.

# Run & test

- [x] Start: python3 server.py.
- [x] Visit http://localhost:8080/ in a browser; expect your index.html.
- [x] Test API: curl -i http://localhost:8080/api/hello (should see JSON and correct headers).
- [x] Test 404: curl -i http://localhost:8080/does-not-exist.

# Platform & port quirks (quick fixes)

- [x] If reuse_port=True isn't supported on your OS, set it to False.
- [x] If you see "Address already in use," pick another port or kill the previous process.
- [x] Ports <1024 may require admin rights; stick to 1024+ for dev.
- [x] If testing across machines, open firewall for the chosen port.

# Minimal hygiene

- [x] Add try/except around parsing to avoid crashing on bad input.
- [x] Cap header size and ignore/close on over-limit input.
- [x] Log request line and status (print is fine for now).

# Nice-to-have next steps (optional)

- [ ] Serve more static files (map /static/... to a directory with MIME detection).
- [ ] Add threading or selectors for concurrency if you expect multiple clients.
- [ ] Implement basic keep-alive (HTTP/1.1) or stick with Connection: close as shown.
- [ ] Return Date and Server headers for completeness (not required).
- [ ] Unit-test handle_request with crafted byte requests.
