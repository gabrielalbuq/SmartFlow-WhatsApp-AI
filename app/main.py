from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import webhook

app = FastAPI(title="Julie - SmartFlow AI")

#Rota
app.include_router(webhook.router)
