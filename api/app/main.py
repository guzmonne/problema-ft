from fastapi import FastAPI
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM

apm = make_apm_client({
    "SERVICE_NAME": "probema-ft-api",
    "DEBUG": True,
    "SERVER_URL": "http://apm:8200",
    "CAPTURE_HEADERS": True,
    "CAPTURE_BODY": "all",
})

app = FastAPI(
    title="Problema FT",
    description="Solución de problema FT",
    version="0.0.1",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(ElasticAPM, client=apm)


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


