# Docker And Containers

Docker packages an app's runtime so it can run consistently outside the local machine setup. It does not replace knowing how the app runs; it makes that runtime explicit.

## Core Concepts And Commands

- Image: blueprint containing runtime, dependencies, app files, and startup command.
- Container: running or stopped instance of an image.
- Docker CLI: `docker` command you type.
- Docker engine: background service that builds images and runs containers.
- Colima: a small Linux VM on macOS that can provide the Docker engine.

Useful commands:

```bash
docker images          # local images
docker ps              # running containers
docker ps -a           # all containers, including stopped ones
docker stop <id/name>  # stop a running container
```

Built images live in Docker's local image store, not as normal project files. Use `docker images` to inspect them.

## Colima On macOS

On macOS, Docker containers still run on Linux. Colima starts a Linux VM and exposes a Docker socket so the normal `docker` CLI can talk to the Docker engine inside that VM.

Useful checks:

```bash
colima status
docker context show
docker ps
docker version
```

What they read:

- `colima status` checks the Colima VM state under `~/.colima/`.
- `docker context show` tells which Docker engine the Docker CLI is targeting.
- `docker ps` asks the active Docker engine for running containers.
- `docker version` confirms both the local Docker client and the Docker server inside Colima are reachable.

If `colima start` fails with a message like:

```text
failed to run attach disk "colima", in use by instance "colima"
```

the important idea is that Colima can be "stopped" from the user's point of view while stale Lima/VM helper processes still hold the VM disk. A safe first repair is:

```bash
colima stop --force
colima start
```

`colima stop --force` stops the stuck runtime and removes stale pid/socket files under `~/.colima/`. It does not delete the Docker disk, so images and containers should remain available. `colima start` starts the VM again and switches the Docker context to `colima`.

After Colima starts, containers from previous work may restart automatically. If a previous container is already using port `8000`, running this todo backend on host port `8000` can fail. Use another host port, such as:

```bash
docker run -p 8001:8000 todo-backend
```

## Backend Dockerfile

Current backend Dockerfile:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

Important mental model: a Dockerfile is a recipe for building an image. During `docker build`, Docker starts from a base image, runs each instruction in order, and saves the result as a new image. Later, `docker run` starts a container from that image.

Some instructions change the filesystem inside the image, such as `COPY` and `RUN`. Other instructions set metadata or defaults, such as `EXPOSE` and `CMD`.

### `FROM python:3.11-slim`

```dockerfile
FROM python:3.11-slim
```

Every Dockerfile needs a starting point. `FROM` chooses the base image.

Breakdown:

- `python`: the image name. This image already contains Python.
- `3.11-slim`: the tag. A tag selects a specific variant of the image.
- `3.11`: use Python 3.11.
- `slim`: use a smaller Linux image than the full Python image.

Why this project uses it: `backend/pyproject.toml` says:

```toml
requires-python = ">=3.11"
```

So the container needs Python 3.11 or newer. Starting from `python:3.11-slim` means the image already has Python installed, instead of us manually installing Python from scratch.

Common confusion: `python:3.11-slim` is not your local Python. It is a Linux-based Python environment downloaded by Docker and used inside the image.

Tradeoff: `slim` keeps the image smaller, but it has fewer operating system tools preinstalled. If a future dependency needs system libraries, the Dockerfile may need extra `apt-get install ...` lines.

### `WORKDIR /app`

```dockerfile
WORKDIR /app
```

`WORKDIR` sets the current directory inside the image.

After this line, later relative paths are interpreted from `/app`.

For example:

```dockerfile
COPY pyproject.toml uv.lock ./
```

means:

```text
copy pyproject.toml and uv.lock into /app/
```

Why this matters: without `WORKDIR`, files might be copied into a less obvious default directory. Setting `/app` gives the image a clean home for this backend.

What it writes: Docker creates `/app` inside the image if it does not already exist.

### `COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/`

```dockerfile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
```

This line adds the `uv` tool to our image.

Normal `COPY` copies files from the build context on your machine into the image. This line is different because it uses `--from=...`.

Breakdown:

- `COPY`: copy files into the image being built.
- `--from=ghcr.io/astral-sh/uv:latest`: copy from another Docker image instead of from the local project folder.
- `ghcr.io`: GitHub Container Registry.
- `astral-sh/uv`: the official image that contains the `uv` binaries.
- `latest`: the tag of that `uv` image.
- `/uv /uvx`: the source files inside the `uv` image.
- `/bin/`: the destination directory inside our backend image.

After this line, our image has:

```text
/bin/uv
/bin/uvx
```

Why `/bin/` matters: `/bin` is normally on the executable search path, called `PATH`. That means later Dockerfile lines can run:

```bash
uv sync --frozen --no-dev
```

instead of needing:

```bash
/bin/uv sync --frozen --no-dev
```

Why this project needs it: dependencies are managed with `uv`, so the Docker image also uses `uv` to install the backend's dependencies.

Common confusion: this does not copy your local `.venv/`. The image installs its own dependencies inside the Linux container environment.

### `COPY pyproject.toml uv.lock ./`

```dockerfile
COPY pyproject.toml uv.lock ./
```

This copies only the dependency files into the image first.

Breakdown:

- `pyproject.toml`: the human-edited dependency/project file.
- `uv.lock`: the exact resolved dependency versions.
- `./`: the destination, meaning the current `WORKDIR`, which is `/app`.

After this line, the image contains:

```text
/app/pyproject.toml
/app/uv.lock
```

Why copy these before copying the rest of the code: Docker can cache build steps. Dependency installation is usually slower than copying source code. By copying dependency files first, Docker only needs to rerun `uv sync` when `pyproject.toml` or `uv.lock` changes.

If `main.py` changes but dependencies do not, Docker can reuse the dependency-install layer and only redo the later `COPY . .` step.

What it reads: these files must exist in the build context. That is why the build command should be run from `backend/`:

```bash
cd backend
docker build -t todo-backend .
```

In that command, `.` means the `backend/` directory is the build context.

### `RUN uv sync --frozen --no-dev`

```dockerfile
RUN uv sync --frozen --no-dev
```

`RUN` executes a command while the image is being built.

This line installs the Python dependencies into the image.

Breakdown:

- `RUN`: build-time command. It happens during `docker build`, not each time the container starts.
- `uv sync`: install the environment described by `pyproject.toml` and `uv.lock`.
- `--frozen`: use the existing `uv.lock` exactly; do not update or rewrite it.
- `--no-dev`: do not install development-only dependencies.

Why `--frozen` matters: Docker builds should be reproducible. If the lockfile says to install specific versions, the image should use those versions instead of silently resolving new ones.

Why `--no-dev` matters: a production-ish image should only contain what it needs to run. Test tools, formatters, and other development dependencies make images larger and add unnecessary packages.

What it reads:

```text
/app/pyproject.toml
/app/uv.lock
```

What it writes: installed dependency files inside the image. With `uv`, this usually means a virtual environment is created in the image, commonly at:

```text
/app/.venv/
```

Common confusion: local `.venv/` is ignored by `.dockerignore`, but the image can still have its own `.venv/`. That is correct. Local virtual environments are machine-specific; container virtual environments are built for the container's Linux environment.

### `COPY . .`

```dockerfile
COPY . .
```

This copies the rest of the backend project into the image.

Breakdown:

- first `.`: source path in the build context on your machine.
- second `.`: destination path inside the image, relative to `WORKDIR`.

Because `WORKDIR` is `/app`, this means:

```text
copy everything allowed from backend/ into /app/
```

The `.dockerignore` file controls what "everything allowed" means.

In this project:

```text
.venv/
__pycache__/
*.py[cod]
```

are excluded from the build context.

Why this line comes after `uv sync`: source code changes more often than dependency files. Keeping `COPY . .` after dependency installation helps Docker reuse the dependency layer when only application code changes.

What gets copied for this backend:

```text
main.py
todo.py
pyproject.toml
uv.lock
Dockerfile
.dockerignore
```

Important detail: `COPY . .` may also copy files that are not needed at runtime unless `.dockerignore` excludes them. That is why `.dockerignore` matters.

### `EXPOSE 8000`

```dockerfile
EXPOSE 8000
```

`EXPOSE` documents which port the app is expected to listen on inside the container.

It does not publish the port to your machine by itself.

Think of it as image metadata:

```text
This containerized app expects to use port 8000 internally.
```

The actual connection from your machine to the container happens at `docker run` time with `-p`:

```bash
docker run -p 8001:8000 todo-backend
```

Meaning:

```text
host port 8001 -> container port 8000
```

Why this project uses `8000`: FastAPI commonly runs on port `8000`, and the `CMD` line starts the server on port `8000`.

Common confusion: `EXPOSE 8000` does not force the app to listen on `8000`. The application command still needs to start the server on that port.

### `CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]`

```dockerfile
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

`CMD` sets the default command that runs when a container starts from the image.

This line does not run during `docker build`. It runs during:

```bash
docker run todo-backend
```

Breakdown:

- `uv`: use the `uv` tool copied earlier into `/bin/`.
- `run`: run a command inside the environment managed by `uv`.
- `fastapi`: the FastAPI command-line program installed as a dependency.
- `run`: FastAPI's production-oriented run command.
- `main.py`: the file containing the FastAPI app.
- `--host`: choose which network interface the server listens on.
- `0.0.0.0`: listen on all container network interfaces.
- `--port`: choose the server port.
- `8000`: listen on port `8000` inside the container.

Why `uv run` is used: it makes sure the command runs with the Python dependencies installed for this project, instead of relying on a globally activated environment.

Why `--host 0.0.0.0` matters: inside a container, `127.0.0.1` would mean "only inside this container." Docker port mapping needs the app to listen on an interface Docker can forward to. `0.0.0.0` allows that.

Why `--port 8000` matters: this matches `EXPOSE 8000` and the container side of `-p 8001:8000`.

The square-bracket form is called exec form:

```dockerfile
CMD ["uv", "run", "fastapi", "run", "main.py"]
```

Each item is one argument. Docker runs the program directly.

The alternative is shell form:

```dockerfile
CMD uv run fastapi run main.py --host 0.0.0.0 --port 8000
```

Exec form is usually preferred for app startup because argument handling and stop signals are cleaner.

### Why The Dockerfile Is Ordered This Way

The order is intentional:

1. Start from a Python base image.
2. Choose `/app` as the application directory.
3. Install the `uv` tool.
4. Copy only dependency files.
5. Install dependencies.
6. Copy the application code.
7. Document the app port.
8. Define the startup command.

The key optimization is steps 4-6. Dependency files change less often than source code, so Docker can often reuse the dependency installation layer.

What to remember: a Dockerfile should make the runtime explicit. For this backend, the runtime needs Python, `uv`, dependency files, app source files, a known port, and a command that starts FastAPI.

## Build Context And .dockerignore

A Docker build does not automatically see your whole computer. It only sees the build context.

In this command:

```bash
docker build -t todo-backend .
```

`.` is the build context. It means:

```text
Send the current directory to Docker as the set of files available during the build.
```

For this project, run the command from `backend/`:

```bash
cd backend
docker build -t todo-backend .
```

Why `backend/` is the right directory:

```text
backend/
  Dockerfile
  .dockerignore
  main.py
  todo.py
  pyproject.toml
  uv.lock
```

The Dockerfile has lines like:

```dockerfile
COPY pyproject.toml uv.lock ./
COPY . .
```

Those source files must exist inside the build context. If you build from the wrong directory, Docker may not find the files where the Dockerfile expects them.

`.dockerignore` keeps machine-local/generated files out of the build context:

```text
.venv/
__pycache__/
*.py[cod]
```

What each pattern means:

- `.venv/`: do not send the local virtual environment to Docker.
- `__pycache__/`: do not send Python bytecode cache folders.
- `*.py[cod]`: do not send generated Python bytecode files such as `.pyc`.

This matters because the local `.venv` is machine-specific and can be large. The image should install its own dependencies with `uv sync` inside the container environment.

What to remember: `.gitignore` controls what Git tracks. `.dockerignore` controls what Docker receives during build. They solve related but separate problems.

## Build Command Walkthrough

The build command creates a Docker image from the Dockerfile.

Run from `backend/`:

```bash
docker build -t todo-backend .
```

Breakdown:

- `docker`: the Docker command-line tool.
- `build`: tell Docker to build an image.
- `-t`: tag/name the image.
- `todo-backend`: the image name we are assigning.
- `.`: use the current directory as the build context.

The command reads:

```text
backend/Dockerfile
backend/.dockerignore
backend/pyproject.toml
backend/uv.lock
backend/main.py
backend/todo.py
```

The command writes:

```text
a Docker image in Docker's local image store
```

It does not create a normal project file called `todo-backend`. Docker images live in Docker's internal storage.

Why `-t todo-backend` matters: the tag gives the image a human-friendly name. Without a tag, Docker can still build the image, but it is harder to refer to later.

After building, inspect the image with:

```bash
docker images todo-backend
```

About image tags: `todo-backend` is shorthand for:

```text
todo-backend:latest
```

`latest` is just a tag name. It does not automatically guarantee this is the newest image in the world; it means this local image has the `latest` tag.

Common build failure:

```text
failed to solve: failed to read dockerfile
```

This usually means Docker cannot find the Dockerfile from the build context. Check that you are in `backend/` or pass the Dockerfile path explicitly.

Another common build failure:

```text
COPY failed: file not found
```

This usually means a `COPY` source is not inside the build context or has a different name than the Dockerfile expects.

## Build-Time Vs Run-Time

A common beginner confusion is the difference between building an image and running a container.

Build-time happens when you run:

```bash
docker build -t todo-backend .
```

During build-time, Docker follows the Dockerfile and creates the image. Instructions like this run during build-time:

```dockerfile
RUN uv sync --frozen --no-dev
```

That means dependencies are installed into the image once while the image is being built.

Run-time happens when you run:

```bash
docker run -p 8001:8000 todo-backend
```

During run-time, Docker starts a container from the already-built image. This instruction provides the default run-time command:

```dockerfile
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

Important difference:

```text
RUN = executes while building the image
CMD = default command when starting a container
```

If you change Python dependencies, rebuild the image. If you only stop and start the same existing image, Docker will not rerun `RUN uv sync ...`.

If you change source code, rebuild the image too. A container does not automatically pick up changed local files unless you use bind mounts, which this project is not using yet.

## Ports, EXPOSE, And Port Mapping

A port is a numbered communication door. In `http://127.0.0.1:8001/docs`, `127.0.0.1` is your machine and `8001` is the host port.

Containers have their own network space, so Docker maps host ports to container ports:

```bash
docker run -p 8001:8000 todo-backend
```

Format:

```text
-p HOST_PORT:CONTAINER_PORT
```

Meaning:

```text
host port 8001 -> container port 8000
```

`EXPOSE 8000` documents the intended container port. `docker run -p ...` performs the actual mapping.

If host port `8000` is already used, this error can appear:

```text
Bind for 0.0.0.0:8000 failed: port is already allocated
```

Fix: use a free host port, such as `8001`, or stop the process/container using `8000`.

Useful checks:

```bash
docker ps
lsof -i :8000
```

## Run Command Walkthrough

The run command starts a container from an image.

Recommended local run command for this project:

```bash
docker run --rm -p 8001:8000 todo-backend
```

Breakdown:

- `docker`: the Docker command-line tool.
- `run`: create and start a container from an image.
- `--rm`: remove the stopped container automatically when it exits.
- `-p`: publish/map a port from your machine to the container.
- `8001:8000`: host port `8001` maps to container port `8000`.
- `todo-backend`: the image to run.

What it reads:

```text
the local Docker image named todo-backend
```

What it starts:

```text
a new container running the Dockerfile's CMD
```

Why `--rm` is useful while learning: each run creates a container. Without `--rm`, stopped containers pile up and appear in:

```bash
docker ps -a
```

For a learning project, `--rm` keeps cleanup simple. Later, when you need to inspect a stopped container, you may intentionally omit `--rm`.

Foreground behavior: this command runs in the foreground. The terminal shows server logs. Press `Ctrl+C` to stop the container.

Detached/background mode:

```bash
docker run -d --name todo-backend-local -p 8001:8000 todo-backend
```

Breakdown of the extra parts:

- `-d`: detached mode, run in the background.
- `--name todo-backend-local`: give the container a human-friendly name.

Detached mode is useful when you want your terminal back, but you then need Docker commands to inspect or stop the container:

```bash
docker logs todo-backend-local
docker stop todo-backend-local
```

Verify after running:

```text
http://127.0.0.1:8001/docs
http://127.0.0.1:8001/tasks
```

The browser talks to host port `8001`. Docker forwards that traffic to container port `8000`, where FastAPI is listening.

## CMD Exec Form Vs Shell Form

Exec form:

```dockerfile
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
```

Shell form:

```dockerfile
CMD uv run fastapi run main.py --host 0.0.0.0 --port 8000
```

Exec form starts the program directly and passes each list item as one argument. Shell form runs through `/bin/sh -c`, which is useful only when shell features like `&&`, pipes, or variable expansion are needed.

Use exec form for normal app startup because signal handling and argument passing are cleaner.

`--host 0.0.0.0` matters in containers: `127.0.0.1` would mean "inside the container only," while `0.0.0.0` listens on interfaces Docker can forward to.

## Common Docker Debugging Commands

These commands help answer specific questions while learning Docker.

### Is Docker Running?

```bash
docker version
docker info
```

`docker version` shows client and server information. If it only shows the client or says it cannot connect to the Docker daemon, the Docker engine is not reachable.

`docker info` asks the Docker server for details. It is a good quick check after starting Colima.

### What Images Exist?

```bash
docker images
docker images todo-backend
```

This reads Docker's local image store. Use it to confirm that `docker build -t todo-backend .` created an image.

### What Containers Are Running?

```bash
docker ps
```

This shows running containers. Use it to confirm whether the backend container is currently running and which ports are mapped.

### What Containers Exist, Including Stopped Ones?

```bash
docker ps -a
```

This shows running and stopped containers. If you run containers without `--rm`, stopped containers remain here.

### What Did A Container Print?

```bash
docker logs <container-name-or-id>
```

This shows logs from a container. For a FastAPI app, logs can show whether the server started successfully or crashed.

Example:

```bash
docker logs todo-backend-local
```

### How Do I Open A Shell Inside A Running Container?

```bash
docker exec -it <container-name-or-id> sh
```

Breakdown:

- `docker exec`: run a command inside an already-running container.
- `-i`: keep standard input open.
- `-t`: allocate a terminal.
- `sh`: start a shell.

Example:

```bash
docker exec -it todo-backend-local sh
```

This is useful for inspecting files inside the container:

```bash
pwd
ls
ls .venv
```

Use this for debugging, not as a normal way to change the app. Changes made manually inside a container are temporary.

### How Do I Stop A Container?

```bash
docker stop <container-name-or-id>
```

Example:

```bash
docker stop todo-backend-local
```

This asks the container to stop gracefully. If the container was started with `--rm`, Docker removes it after it stops.

## Local Build And Run Flow

From `backend/`:

```bash
docker build -t todo-backend .
docker images todo-backend
docker run --rm -p 8001:8000 todo-backend
```

What each step proves:

- `docker build -t todo-backend .`: the Dockerfile can produce an image.
- `docker images todo-backend`: the image exists locally.
- `docker run --rm -p 8001:8000 todo-backend`: the image can start as a container and accept traffic through a mapped port.

Verify:

```text
http://127.0.0.1:8001/docs
http://127.0.0.1:8001/tasks
```

What to remember: image = blueprint; container = instance; `docker build` creates image; `docker run` creates/runs container; `-p` connects host networking to container networking.

## Docker Setup Checklist Before Deployment

Before choosing a deployment service, this backend should pass a local Docker checklist.

Current status in this project:

- File setup is complete: `backend/Dockerfile` and `backend/.dockerignore` both exist.
- The Dockerfile defines a portable FastAPI runtime using Python, `uv`, the locked dependencies, app source files, port `8000`, and a startup command.
- `.dockerignore` excludes local/generated Python files from the build context.
- The remaining Docker checkpoint is local verification: build the image, run a container, and confirm the API responds through a mapped host port.

File setup:

- `backend/Dockerfile` exists.
- `backend/.dockerignore` exists.
- `.dockerignore` excludes `.venv/`, `__pycache__/`, and Python bytecode files.
- `backend/pyproject.toml` and `backend/uv.lock` are committed so dependencies are reproducible.

Build checks:

- Run from `backend/`.
- `docker build -t todo-backend .` completes successfully.
- `docker images todo-backend` shows the image.

Run checks:

- `docker run --rm -p 8001:8000 todo-backend` starts the app.
- `http://127.0.0.1:8001/docs` loads the FastAPI docs.
- `http://127.0.0.1:8001/tasks` returns JSON.
- The app listens on `0.0.0.0` inside the container.
- The container uses port `8000` internally.

Common readiness issues:

- Docker daemon is not running. On this Mac setup, start/check Colima.
- Host port is already in use. Try host port `8001` or stop the process/container using the port.
- Build context is wrong. Run `docker build` from `backend/`.
- Local `.venv/` is accidentally sent to Docker. Check `.dockerignore`.

What to remember: local Docker success does not guarantee deployment will be effortless, but it proves the app has a portable runtime that a deployment service can start.
