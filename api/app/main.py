from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, HTMLResponse
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM

from .items import Items
from .meli import Meli
from .models.item import Item
from .models.domain import Domain
from .models.ft import FT


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

meli = Meli()
items = Items()

@app.get("/api/items/{item_id}", response_model=FT)
def read_item(item_id: str):
    return items.get_item(item_id)

@app.get("/api/meli/items/{item_id}", response_model=Item)
def read_meli_item(item_id: str):
    return meli.get_item(item_id)

@app.get("/api/meli/domains/{domain_id}", response_model=Domain)
def read_meli_domain(domain_id: str):
    return meli.get_domain(domain_id)