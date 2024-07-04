from fastapi import FastAPI

from .routers import stripe

app = FastAPI()

app.include_router(stripe.router, prefix='/stripe')