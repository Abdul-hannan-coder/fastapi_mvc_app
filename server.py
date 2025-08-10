

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from database.database import MONGO_URI
from routes.contact_routes import api_router as contact_router
from routes.view_routes import router as view_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mongo_client = AsyncIOMotorClient(MONGO_URI)
    app.state.db = app.state.mongo_client["Contact_Project"]
    print("MongoDB connected")
    yield
    app.state.mongo_client.close()
    print("MongoDB connection closed")

app = FastAPI(lifespan=lifespan)

# Serve static files under /static URL
app.mount("/static", StaticFiles(directory="assets"), name="static")

# UI routes (e.g., templates, form pages, listing)
app.include_router(contact_router, prefix="/contacts")

# Additional UI or API routes
app.include_router(view_router)
