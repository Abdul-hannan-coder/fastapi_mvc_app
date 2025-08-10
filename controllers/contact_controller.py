from fastapi import HTTPException
from bson import ObjectId
from utils.helper import serialize_contact 

from models.contact_model import ContactModel
from motor.motor_asyncio import AsyncIOMotorDatabase

async def delete_contact(db: AsyncIOMotorDatabase, contact_id: str):
    if not ObjectId.is_valid(contact_id):
        raise HTTPException(status_code=400, detail="Invalid contact ID")

    result = await db.users.delete_one({"_id": ObjectId(contact_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {"message": "Contact deleted successfully"}

async def get_all_contacts(db: AsyncIOMotorDatabase):
    contacts_cursor = db.users.find()
    contacts = []
    async for contact in contacts_cursor:
        contacts.append(serialize_contact(contact))
    return contacts

async def create_contact(db: AsyncIOMotorDatabase, contact: ContactModel):
    existing = await db.users.find_one({
        "$or": [
            {"email": contact.email},
            {"phone": contact.phone},
            {"fname": contact.fname}
        ]
    })
    if existing:
        raise HTTPException(status_code=400, detail="Email, phone, or name already exists")

    contact_dict = contact.model_dump()
    contact_dict.pop("id", None)

    result = await db.users.insert_one(contact_dict)
    new_contact = await db.users.find_one({"_id": result.inserted_id})
    return serialize_contact(new_contact)

async def update_contact(db: AsyncIOMotorDatabase, contact_id: str, contact_data: ContactModel):
    if not ObjectId.is_valid(contact_id):
        raise HTTPException(status_code=400, detail="Invalid contact ID")

    update_data = contact_data.model_dump(exclude={"id"})
    result = await db.users.update_one({"_id": ObjectId(contact_id)}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")

    updated_contact = await db.users.find_one({"_id": ObjectId(contact_id)})
    return serialize_contact(updated_contact)

async def get_contact_by_id(db: AsyncIOMotorDatabase, contact_id: str):
    if not ObjectId.is_valid(contact_id):
        raise HTTPException(status_code=400, detail="Invalid contact ID")

    contact = await db.users.find_one({"_id": ObjectId(contact_id)})
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    return serialize_contact(contact)
