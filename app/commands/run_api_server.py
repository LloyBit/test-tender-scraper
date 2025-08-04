from typer import Typer
from fastapi import FastAPI
import uvicorn
from ..api.tenders import router as tender_router


hoster_app = Typer()

app = FastAPI()
app.include_router(tender_router)

@hoster_app.command("host")
def runserver(host: str = "127.0.0.1", port: int = 8000):
    uvicorn.run("app.commands.run_api_server:app", host=host, port=port, reload=True)