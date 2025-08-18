# 0 Project prep

- [x] Create a project folder with:
    - [x] `index.html` (your portfolio page)
    - [x] A place for your server source file
    - [x] Optional: a `static/` folder for future assets (css/js/img)
- [ ] Decide host/port (e.g., `0.0.0.0:8080`)
- [ ] Decide routes you'll support:
    - [ ] `/` (serve `index.html`)
    - [ ] `/api/hello` (return JSON)

# 1 Open the listening socket

- [ ] Create TCP server socket (IPv4/IPv6 as you prefer)
- [ ] Set reuse options (e.g., `SO_REUSEADDR`, optionally `SO_REUSEPORT`)
- [ ] Bind to host/port and `listen(backlog)`
- [ ] Print a startup banner with the URL

**Acceptance:** `netstat`/`ss` shows the port listening; no crash on start.

# 2 Accept connections loop

- [ ] `accept()` a client and obtain `(conn, addr)`
- [ ] Wrap connection handling in a `try/finally` to **always** close the socket
- [ ] (Single-threaded is fine to start; one request at a time)

**Acceptance:** Incoming connections don't crash the server even if the client disconnects early.

# 3 Read the HTTP request (headers only)

- [ ] Initialize a buffer `buf = empty`
- [ ] Repeatedly `recv()` until you find `\r\n\r\n` (end of headers) **or** hit:
    - [ ] A max header size limit (e.g., 64 KiB) → if exceeded, plan to return `431 Request Header Fields Too Large` or `400`
    - [ ] A read timeout (optional for v1, add later)
- [ ] If the client closes before you get headers, handle gracefully

**Acceptance:** For a basic GET, the full request head is captured and you stop reading.

# 4 Parse the request line (only)

- [ ] Split the header block on `\r\n`; take the **first line** as the request line
- [ ] Extract:
    - [ ] `method` (expect `GET` only)
    - [ ] `path` (e.g., `/`, `/api/hello`, possibly `/index.html`)
    - [ ] `http_version` (e.g., `HTTP/1.1`) – you don't need to use it yet
- [ ] If parsing fails → return `400 Bad Request`
- [ ] If `method != GET` → return `405 Method Not Allowed` with a plain-text body
- [ ] Parse request headers to extract `Accept-Language` for localization (v1.1)

**Acceptance:** A malformed request yields `400`; non-GET yields `405`.

# 5 Basic routing

- [ ] If `path == "/"` or `"/index.html"` → serve `index.html` (static for v1)
- [ ] If `path == "/api/hello"` → serve a small JSON payload
- [ ] Everything else → return `404 Not Found`

**Acceptance:** `curl /`, `curl /index.html`, and `curl /api/hello` each produce expected outcomes; unknown path → 404.

# 6 Prepare response bodies

- [ ] Load `index.html` **once at startup** into memory (bytes) for v1
- [ ] Prepare JSON for `/api/hello` (e.g., `{"message":"...","ok":true}`) as bytes
- [ ] Decide default error bodies (`bad request`, `not found`, etc.)

**Acceptance:** You can construct the needed response bodies without file I/O on every request.

# 7 Build an HTTP response function

- [ ] Inputs: `status` (e.g., `"200 OK"`), `content_type`, and `body` (bytes)
- [ ] Always include headers:
    - [ ] `Content-Type: <value>` (e.g., `text/html; charset=utf-8`, `application/json; charset=utf-8`, `text/plain; charset=utf-8`)
    - [ ] `Content-Length: <len(body)>` (must be exact)
    - [ ] `Connection: close`
- [ ] Format: status line + headers (CRLF-terminated) + blank line + body
- [ ] Return the complete byte sequence ready to `sendall()`

**Acceptance:** `curl -i` shows correct status line, headers, and body; body length matches.

# 8 Send the response

- [ ] For each connection:
    - [ ] Read headers into `buf`
    - [ ] Build response according to routing
    - [ ] `sendall()` the full response
    - [ ] Close the connection
- [ ] Ignore keep-alive; you're doing one-shot requests for v1

**Acceptance:** `ab`/`wrk` light testing shows consistent responses and no lingering connections after completion.

# 9 MIME and small niceties (v1.1 of your server)

- [ ] Ensure `index.html` uses `text/html; charset=utf-8`
- [ ] Return a minimal `favicon.ico` or a `404` that doesn't spam logs
- [ ] Include `Date` header (optional)
- [ ] Normalize `\n` vs `\r\n` safely in your own output (must use `\r\n`)

**Acceptance:** Browsers don't complain; no endless `favicon.ico` errors.

# 10 Error handling policy

- [ ] `400 Bad Request` for malformed request line
- [ ] `405 Method Not Allowed` for non-GET
- [ ] `404 Not Found` for unknown paths
- [ ] `431` or `400` if header block exceeds your cap
- [ ] Catch-all try/catch to return `500 Internal Server Error` on unexpected exceptions

**Acceptance:** You can trigger each error path via `curl` and get the intended status.

# 11 Logging (basic)

- [ ] On each request, log:
    - [ ] Remote address
    - [ ] Method + path
    - [ ] Status code
    - [ ] Response size (bytes)
    - [ ] Duration (ms) (optional)
- [ ] On startup/shutdown, log a clear message

**Acceptance:** You can read logs and reconstruct basic traffic.

# 12 Graceful shutdown

- [ ] Handle an interrupt signal (`SIGINT`) to:
    - [ ] Stop accepting new connections
    - [ ] Close the listening socket
    - [ ] Let an in-flight request finish (if you later add concurrency)
- [ ] Print a clean shutdown message

**Acceptance:** Ctrl-C exits cleanly without stack traces or port leaks.

# 13 Manual tests

- [ ] `curl -i http://localhost:8080/`
- [ ] `curl -i http://localhost:8080/api/hello`
- [ ] `curl -i http://localhost:8080/does-not-exist`
- [ ] `curl -i -X POST http://localhost:8080/` → expect `405`
- [ ] Browser test at `http://localhost:8080/` renders your page

**Acceptance:** All return expected HTTP statuses and bodies.

# 14 Dynamic HTML generation (v2 enhancement)

- [ ] Create a simple templating system for `index.html`
- [ ] Generate content dynamically instead of serving static file
- [ ] Support placeholders for content insertion
- [ ] Extract common layout elements (header, footer) 
- [ ] Support template inheritance or includes

**Acceptance:** Dynamic HTML pages render correctly with appropriate content.

# 15 Localization with i18n (v2 enhancement)

- [ ] Create localization files:
   - [ ] Establish directory structure (e.g., `/locales/en/`, `/locales/es/`)
   - [ ] Create JSON/YAML translation files for supported languages
   - [ ] Include translations for UI text and messages
- [ ] Implement language detection:
   - [ ] Parse `Accept-Language` header from requests
   - [ ] Support language URL prefix (e.g., `/es/`, `/en/`)
   - [ ] Implement fallback language mechanism
- [ ] Integrate with dynamic HTML:
   - [ ] Replace hardcoded strings with translation keys
   - [ ] Select appropriate translations when rendering templates
   - [ ] Add language switcher to UI

**Acceptance:** Users see content in their preferred language; language can be changed via URL or UI.

# 16 Optional: static file serving

- [ ] Add route prefix `/static/`
- [ ] Map path to `./static/<rest>`
- [ ] Prevent path traversal (`..`)
- [ ] Guess `Content-Type` from extension (html, css, js, png, jpg, svg)
- [ ] Add `Cache-Control` headers (e.g., long TTL for hashed assets)

**Acceptance:** `curl -I` shows correct types; assets load in the browser.

# 17 Optional: simple query parsing

- [ ] Parse `?name=...` for an endpoint like `/api/hello?name=Ana`
- [ ] Return JSON with that value
- [ ] Set default when missing

**Acceptance:** Query param is reflected safely in JSON.

# 18 Optional: timeouts & safety (hardening)

- [ ] Header read timeout (e.g., 5–10s)
- [ ] Max header size (already added)
- [ ] Limit concurrent clients (if you add concurrency)
- [ ] Input validation on paths
- [ ] Basic rate limiting (later, if needed)

**Acceptance:** Slowloris attempts don't hang the server indefinitely.

# 19 Cloudflare front (when you deploy)

- [ ] Choose one:
    - [ ] **DNS (orange cloud)** to your server's IP
    - [ ] **Cloudflare Tunnel** to `http://localhost:8080`
- [ ] Cloudflare settings:
    - [ ] SSL mode: **Full** (or **Full (strict)** if you later add TLS at origin)
    - [ ] **Always Use HTTPS** enabled
    - [ ] **Brotli** + **Auto Minify** on
    - [ ] Cache rule for static files (optional; set proper `Cache-Control` at origin)
- [ ] Firewall: restrict direct origin access to Cloudflare IP ranges (if public)

**Acceptance:** Your domain serves via HTTPS, and direct origin IP isn't publicly reachable (or is tunnel-only).

# 20 Stretch goals

- [ ] Add a tiny **health endpoint** (`/healthz`) returning `200 OK`
- [ ] Add a **/api/time** endpoint with server time in JSON
- [ ] Add minimal **CORS** headers for your API (if you'll call it from a different origin)
- [ ] Swap to a **thread-per-connection** or **async** model to learn concurrency
- [ ] Instrument simple **metrics** (request count, latency, 5xx count)
- [ ] Support content negotiation via `Accept-Language` with quality values
- [ ] Implement language-specific SEO metadata
