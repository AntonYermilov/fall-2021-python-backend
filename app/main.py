from fastapi import FastAPI
from app.routers import sample_index

app = FastAPI()
app.include_router(sample_index.router)
