from fastapi import FastAPI
from src.routers import reports

app = FastAPI()

app.include_router(reports.router, prefix="/api")