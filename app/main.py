from fastapi import FastAPI

from config.config import init_database
from api import template as template_api
from api import render as render_api

app = FastAPI()

@app.on_event("startup")
async def start_database():
    await init_database()


@app.get("/")
def read_root():
    return {"message": "Template renderer"}


app.include_router(
    template_api.router,
    prefix="/template",
)
app.include_router(
    render_api.router,
    prefix="/render",
)
