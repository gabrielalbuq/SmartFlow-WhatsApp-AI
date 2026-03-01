from fastapi import FastAPI
from app.routers import webhook

app = FastAPI(title="Julie - SmartFlow AI")

app.include_router(webhook.router)