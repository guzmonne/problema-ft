from fastapi import FastAPI

app = FastAPI(
    title="Problema FT",
    description="Solución de problema FT",
    version="0.0.1",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


@app.get("/api/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/api/callback")
def auth_callback():
    return {"ok": "go"}

@app.get("/api/notifications")
def read_notifications():
    return {"ok": "go"}


