# Networking, Clients, Servers, And Ports

This topic explains the networking ideas that show up when running the FastAPI backend locally, inside Docker, and eventually in deployment.

## Client And Server

A client is the program that asks for something.

Examples:

- a browser visiting `/docs`;
- Swagger UI sending a request from the browser;
- `curl` in a terminal;
- a future React frontend;
- another backend service.

A server is the program that listens for requests and sends responses.

In this project:

```text
client  ->  HTTP request  ->  FastAPI server
client  <-  HTTP response <-  FastAPI server
```

The FastAPI app is the server. It waits for HTTP requests such as:

```text
GET /tasks
POST /tasks
```

Important idea: the client does not directly call Python functions. The client sends an HTTP request, and FastAPI maps that request to a Python route function.

## URL Pieces

Example URL:

```text
http://127.0.0.1:8001/tasks
```

Breakdown:

- `http`: the protocol. It tells the client how to communicate.
- `127.0.0.1`: the host. It tells the client which machine to contact.
- `8001`: the port. It tells the client which server process on that machine to contact.
- `/tasks`: the path. It tells the server which route/resource is being requested.

Mental model:

```text
protocol://host:port/path
```

If the URL is:

```text
http://127.0.0.1:8001/docs
```

the browser is saying:

```text
Use HTTP.
Contact my own machine.
Use port 8001.
Ask for /docs.
```

## Where IP Addresses Come From

An IP address belongs to a network interface, not directly to an app.

A network interface is a way the machine can send or receive network traffic. Examples:

- loopback interface: internal traffic back to the same machine;
- Wi-Fi interface: traffic through your wireless network;
- Ethernet interface: traffic through a cable;
- Docker/Colima virtual interfaces: traffic between your machine and containers.

The operating system manages these interfaces and their IP addresses.

Common local addresses:

```text
127.0.0.1
localhost
0.0.0.0
```

`127.0.0.1` is built into the networking stack as the loopback address. It means:

```text
send this traffic back to this same machine
```

No router or internet connection is needed for `127.0.0.1`.

`localhost` is a name that usually resolves to `127.0.0.1`.

These two are usually equivalent for local development:

```text
http://127.0.0.1:8001/tasks
http://localhost:8001/tasks
```

Your Wi-Fi IP address is different. It is usually assigned by your router using DHCP. It might look like:

```text
192.168.1.25
```

That address means "this machine on this local network." Other devices on the same network may be able to reach it, depending on firewall and server settings.

`0.0.0.0` is not a normal destination you type into the browser. Servers use it while binding/listening to mean:

```text
listen on all available network interfaces
```

You usually do not visit this in the browser:

```text
http://0.0.0.0:8000
```

Instead, a server binds/listens on `0.0.0.0`, and a client connects through a reachable address such as `127.0.0.1`.

What to remember:

```text
IP address = which network interface/machine
127.0.0.1 = this same machine
0.0.0.0 = server listens on all interfaces
```

## Where Ports Come From

A port is a number managed by the operating system. It helps the OS deliver network traffic to the right process.

Ports are not physical plugs. They are software numbers from:

```text
0 to 65535
```

When a server starts, it asks the OS to bind to an IP address and port.

Example:

```bash
fastapi run main.py --host 0.0.0.0 --port 8000
```

Meaning:

```text
FastAPI asks the OS:
"Please send me traffic that arrives on port 8000."
```

The OS keeps a table of listening processes. Conceptually:

```text
IP/interface        port    process
0.0.0.0             8000    FastAPI
127.0.0.1           5432    database
127.0.0.1           5173    React dev server
```

When a request arrives, the OS looks at the destination IP and destination port, then forwards the traffic to the matching process.

Examples:

```text
FastAPI dev server      -> port 8000
Docker-mapped backend   -> port 8001 on your machine
React dev server        -> often port 5173 or 3000
```

One machine can run many server programs at once because they listen on different ports.

In:

```text
http://127.0.0.1:8001/tasks
```

`8001` tells the browser which local port to contact.

Common confusion: the path `/tasks` does not choose the process. The port chooses the process. After the request reaches the server process, the path chooses the route inside that server.

Another common confusion: two servers usually cannot bind the exact same IP address, port, and protocol at the same time. That is why you see "port already in use" errors.

What to remember:

```text
IP address gets traffic to the machine/interface.
Port gets traffic to the right process on that machine.
Path gets traffic to the right route inside the web app.
```

## Binding Vs Connecting

Servers bind to an address and port. Clients connect to an address and port.

FastAPI command:

```bash
fastapi run main.py --host 0.0.0.0 --port 8000
```

Server meaning:

```text
Start the FastAPI app.
Listen on all container interfaces.
Use port 8000.
```

Browser URL:

```text
http://127.0.0.1:8001/tasks
```

Client meaning:

```text
Connect to my own machine.
Use port 8001.
Ask for /tasks.
```

What to remember:

```text
server binds/listens
client connects/requests
```

## Why Docker Has Two Ports

Containers have their own network space. A server inside a container can listen on port `8000`, while your machine exposes a different port such as `8001`.

Command:

```bash
docker run --rm -p 8001:8000 todo-backend
```

Breakdown:

```text
-p HOST_PORT:CONTAINER_PORT
-p 8001:8000
```

Meaning:

```text
your machine port 8001 -> container port 8000
```

Request flow:

```text
browser
  -> http://127.0.0.1:8001/tasks
  -> Docker receives traffic on host port 8001
  -> Docker forwards it to container port 8000
  -> FastAPI handles GET /tasks
  -> response travels back to browser
```

Why not use `8000:8000` every time? You can, but only if host port `8000` is free. If another server or container is already using host port `8000`, use another host port:

```bash
docker run --rm -p 8001:8000 todo-backend
```

The container can still use port `8000` internally.

## Why Containers Need `0.0.0.0`

Inside a container, this is usually wrong for web servers:

```bash
--host 127.0.0.1
```

`127.0.0.1` inside the container means:

```text
only listen inside this container
```

Docker port forwarding may not be able to reach a server that only listens on the container's own loopback address.

This is why the Dockerfile uses:

```dockerfile
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

`0.0.0.0` means the FastAPI server listens on interfaces that Docker can forward traffic to.

What to remember:

```text
Inside Docker server command: use 0.0.0.0
In your browser: use 127.0.0.1 or localhost
```

## Local Development Vs Docker

Without Docker, you may run FastAPI directly:

```bash
uv run fastapi dev main.py
```

Then you might visit:

```text
http://127.0.0.1:8000/docs
```

Flow:

```text
browser -> host port 8000 -> FastAPI running directly on your machine
```

With Docker:

```bash
docker run --rm -p 8001:8000 todo-backend
```

Then you visit:

```text
http://127.0.0.1:8001/docs
```

Flow:

```text
browser -> host port 8001 -> Docker -> container port 8000 -> FastAPI inside container
```

The browser still talks to your machine. Docker adds a forwarding step between your machine and the container.

## Common Problems

### Port Already In Use

Error shape:

```text
Bind for 0.0.0.0:8000 failed: port is already allocated
```

Meaning: something on your machine is already using host port `8000`.

Fix options:

```bash
docker run --rm -p 8001:8000 todo-backend
```

or stop the process/container using port `8000`.

### Server Started But Browser Cannot Connect

Check:

- Is the server running?
- Is Docker running?
- Did you use the correct host port in the browser?
- Is the app listening on `0.0.0.0` inside the container?
- Did the container crash after starting?

Useful commands:

```bash
docker ps
docker logs <container-name-or-id>
```

### Confusing Host Port And Container Port

In:

```bash
docker run --rm -p 8001:8000 todo-backend
```

use this in the browser:

```text
http://127.0.0.1:8001/docs
```

Do not use this unless you mapped host port `8000`:

```text
http://127.0.0.1:8000/docs
```

What to remember: the browser uses the host port, not the container port.

## What Changes In Deployment

Local development uses addresses like:

```text
127.0.0.1
localhost
```

Deployment uses a public or cloud-provided address, such as:

```text
https://your-app.example.com
```

The basic idea is the same:

```text
client -> address + port/path -> server -> response
```

The difference is that a deployment platform usually handles public networking, HTTPS, routing, and port exposure for you. The app still needs to listen on the port and host expected by the platform.

What to remember: Docker teaches the same client/server and port concepts you will need for deployment. Deployment adds a public address and platform-managed networking.
