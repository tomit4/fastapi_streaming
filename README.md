# FastAPI/SolidJS Image Streaming Proof Of Concept

This repo contains a proof of concept around streaming images from a FastAPI
backend server to a SolidJS frontend.

## Starting the Servers

You'll need to open two terminals. One for backend and frontend.

Within backend:

```sh
rye run dev
```

And on the frontend:

```sh
bun dev
```

In your browser open localhost:3000, and you should see your images stream in.
The logic for the backend lives in ./backend/src/fastapi_app/routers/users.py.
And the logic for the frontend lives in ./frontend/src/App.tsx.
