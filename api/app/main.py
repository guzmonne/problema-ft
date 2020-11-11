from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, HTMLResponse
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
from .meli import Meli

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

m = Meli()

@app.get("/api/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/authorize", response_class=HTMLResponse)
def get_meli_tokens():
    return f"""
    <html>
        <head><title>Problema FT</title></head>
        <body>
            Go to <a href="{m.authorization_url}">this link</a>
            to authorize the app.
        </body>
    </html>
    """

@app.get("/api/items/{item_id}")
def read_item(item_id: str):
    return m.get_item(item_id)

@app.get("/api/callback", response_class=PlainTextResponse)
def auth_callback(code: str = None):
    if code == None:
        return "No code was supplied"
    return m.get_authorization_token(code)

@app.get("/api/notifications")
def read_notifications():
    return {"ok": "go"}

@app.get("/api/user")
def read_authenticated_user():
    return dict(
        user_id=m.user_id,
        scope=m.scope,
        expires_in=m.expires_in,
    )
