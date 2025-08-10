def serialize_contact(contact: dict) -> dict:
    contact["id"] = str(contact["_id"])
    contact.pop("_id", None)
    return contact
