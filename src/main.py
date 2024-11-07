from fastapi import FastAPI
from src.routers import reports, filters

app = FastAPI()

app.include_router(reports, prefix="/api")
app.include_router(filters, prefix="/api/filter")