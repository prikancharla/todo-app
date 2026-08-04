# Deployment On Render

Deployment means running the backend somewhere outside the local machine so clients can reach it through a public URL.

For this project, Render is the first deployment target because it can build and run a web service from the repo and can use the backend Dockerfile.

## Current Deployment Result

The first Render deployment works.

The important debugging moment was seeing:

```json
{"detail":"Not Found"}
```

at the base URL. That did not mean the deployment failed. It meant the deployed FastAPI app was running, but the app has no `/` route.

The correct verification paths are:

```text
/docs
/tasks
```

What to remember: when a backend is deployed, always test a route the app actually defines. The public service URL is only the host; it still needs the correct path.

## Public URL Paths

A deployed FastAPI app has the same routes as the local app.

Current routes:

```text
GET    /tasks
POST   /tasks
GET    /tasks/{uid}
DELETE /tasks/{uid}
PATCH  /tasks/{uid}/toggle
```

FastAPI also provides docs at:

```text
/docs
```

There is currently no route for:

```text
/
```

So visiting only the base Render URL can return:

```json
{"detail":"Not Found"}
```

That response means FastAPI received the request, but no route matched `/`. It is different from a failed deployment. To verify this backend, use:

```text
https://<render-service-url>/docs
https://<render-service-url>/tasks
```

What to remember: a public deployment URL is just the host. The API path still matters.

## Render Port Binding

A web service must listen on a port so Render can forward internet traffic to it.

Render provides a `PORT` environment variable for web services. The default is usually:

```text
10000
```

Render's FastAPI example starts the server using that variable:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

The important idea is not that every app must use port `8000`. The important idea is:

```text
The app must listen on the same port Render forwards traffic to.
```

In local Docker runs, this project has used:

```bash
docker run --rm -p 8001:8000 todo-backend
```

Meaning:

```text
host port 8001 -> container port 8000
```

On Render, there is no `docker run -p 8001:8000` command that the user types. Render handles public routing. The container only needs to bind to the port Render expects.

## Docker Runtime Vs Native Python Runtime

Render can deploy this backend in more than one way:

- Docker runtime: Render builds and runs `backend/Dockerfile`.
- Native Python runtime: Render installs Python dependencies and uses a start command such as `uvicorn ...`.

For this learning project, use Docker runtime if the goal is to deploy the Docker image setup.

Important Render service settings for Docker:

```text
Runtime / Language: Docker
Root Directory: backend
Dockerfile Path: Dockerfile
Docker Command: empty unless intentionally overriding CMD
```

Why `Docker Command` usually stays empty: if it is set, Render runs that command instead of the `CMD` in the Dockerfile. That can make the deployed service behave differently from the image tested locally.

## Debugging `{"detail":"Not Found"}`

If the deployed URL returns:

```json
{"detail":"Not Found"}
```

check the path first.

Expected:

```text
https://<render-service-url>/docs
https://<render-service-url>/tasks
```

Expected but not useful yet:

```text
https://<render-service-url>/
```

Why: there is no `@app.get("/")` route in `backend/main.py`.

What to remember: FastAPI's `404 Not Found` can mean the app is running correctly but the requested path does not exist.

## Deployment Verification Checklist

After each Render deploy:

1. Check the deploy logs for a successful build.
2. Check that the server starts without crashing.
3. Confirm which port the server is listening on.
4. Visit `/docs`.
5. Visit `/tasks`.
6. Try a simple `POST /tasks` from `/docs`.

For this project, deployment is successful when:

```text
/docs loads
/tasks returns JSON
POST /tasks creates an in-memory task
```

Known limitation: because the todo list is still in memory, deployed data can reset whenever Render restarts or redeploys the service.
