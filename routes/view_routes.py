from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from controllers.contact_controller import get_all_contacts, delete_contact, get_contact_by_id, create_contact , update_contact
from models.contact_model import ContactModel
templates = Jinja2Templates(directory="views")
router = APIRouter(prefix="/contacts")


@router.get("/create", response_class=HTMLResponse)
async def create_contact_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

from models.contact_model import ContactModel

@router.post("/create")
async def create_contact_route(
    request: Request,
    fname: str = Form(...),
    lname: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...)
):
    db = request.app.state.db
    contact = ContactModel(
        fname=fname,
        lname=lname,
        email=email,
        phone=phone,
        address=address
    )
    await create_contact(db, contact)
    return RedirectResponse(url="/contacts", status_code=303)


@router.get("/", response_class=HTMLResponse)
async def contacts_page(request: Request):
    db = request.app.state.db
    contacts = await get_all_contacts(db)
    return templates.TemplateResponse("index.html", {"request": request, "contacts": contacts})


@router.post("/delete/{contact_id}")
async def delete_contact_route(request: Request, contact_id: str):
    db = request.app.state.db
    await delete_contact(db, contact_id)
    return RedirectResponse(url="/contacts", status_code=303)


@router.get("/show/{contact_id}", response_class=HTMLResponse)
async def show_contact_page(request: Request, contact_id: str):
    db = request.app.state.db
    contact = await get_contact_by_id(db, contact_id)
    if not contact:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("show.html", {"request": request, "contact": contact})



@router.get("/edit/{contact_id}", response_class=HTMLResponse)
async def edit_contact_form(request: Request, contact_id: str):
    db = request.app.state.db
    contact = await get_contact_by_id(db, contact_id)
    if not contact:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("form.html", {"request": request, "contact": contact, "edit": True})

@router.post("/edit/{contact_id}")
async def edit_contact_route(
    request: Request,
    contact_id: str,
    fname: str = Form(...),
    lname: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...)
):
    db = request.app.state.db
    # Prepare updated contact model or dict
    updated_contact = ContactModel(
        fname=fname,
        lname=lname,
        email=email,
        phone=phone,
        address=address
    )
    await update_contact(db, contact_id, updated_contact)
    return RedirectResponse(url="/contacts", status_code=303)
