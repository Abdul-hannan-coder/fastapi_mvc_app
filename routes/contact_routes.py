from fastapi import APIRouter, Request
from controllers.contact_controller import (
    get_all_contacts,
    delete_contact,
    update_contact,
    create_contact,
    get_contact_by_id,
)
from models.contact_model import ContactModel
api_router = APIRouter(
    prefix="/api/contacts",
    tags=["contacts"]
)

@api_router.get("/", response_model=list[ContactModel])
async def list_contacts_api(request: Request):
    db = request.app.state.db
    return await get_all_contacts(db)

@api_router.post("/", response_model=ContactModel)
async def add_contact_api(request: Request, contact: ContactModel):
    db = request.app.state.db
    return await create_contact(db, contact)

@api_router.get("/delete/{contact_id}")
async def delete_contact_api(request: Request, contact_id: str):
    db = request.app.state.db
    return await delete_contact(db, contact_id)

@api_router.put("/{contact_id}", response_model=ContactModel)
async def update_contact_api(request: Request, contact_id: str, contact: ContactModel):
    db = request.app.state.db
    return await update_contact(db, contact_id, contact)

@api_router.get("/{contact_id}", response_model=ContactModel)
async def get_contact_api(request: Request, contact_id: str):
    db = request.app.state.db
    return await get_contact_by_id(db, contact_id)
