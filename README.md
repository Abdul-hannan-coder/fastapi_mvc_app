Contact App - Project Documentation

Contact Management App - Project Documentation
==============================================

This documentation explains the Contact Management App built using **FastAPI** (backend) and **Jinja2** templates (frontend). It covers setup, routing, templates, database interactions, and how to run the project.

1\. Project Overview
--------------------

*   A CRUD web app to manage contacts: Create, Read, Update, Delete contacts.
*   Backend implemented with `FastAPI`, serving HTML responses using `Jinja2Templates`.
*   Data stored in a MongoDB database, accessed asynchronously.
*   Frontend uses Bootstrap 4 for styling and responsive layout.

2\. Folder Structure
--------------------

*   `main.py` - FastAPI app entry point and route mounting.
*   `routers/contacts.py` - Contains all routes related to contacts.
*   `controllers/contact_controller.py` - Business logic for CRUD operations.
*   `models/contact_model.py` - Data model for Contact using Pydantic.
*   `views/` - Jinja2 HTML templates for rendering pages.
*   `static/assets/` - CSS and other static assets (Bootstrap, FontAwesome, custom CSS).

3\. Installation and Setup
--------------------------

To get the project running locally, follow these steps:

    # Clone the repo
    git clone <your-github-repo-url>
    cd <repo-folder>
    
    # Create virtual environment (optional but recommended)
    python3 -m venv venv
    source venv/bin/activate    # Linux/macOS
    venv\Scripts\activate       # Windows
    
    # Install dependencies
    pip install fastapi uvicorn motor jinja2
    
    # Start the FastAPI server
    uvicorn main:app --reload
    

\- The server will be running by default at [http://127.0.0.1:8000](http://127.0.0.1:8000). - MongoDB connection should be configured in `main.py` or your app settings.

4\. Routing
-----------

*   `GET /contacts` - List all contacts.
*   `GET /contacts/create` - Show form to create a new contact.
*   `POST /contacts/create` - Submit new contact data and save to DB.
*   `GET /contacts/edit/{contact_id}` - Show form to edit existing contact (pre-filled).
*   `POST /contacts/edit/{contact_id}` - Submit updated data to update the contact.
*   `POST /contacts/delete/{contact_id}` - Delete a contact by ID.
*   `GET /contacts/show/{contact_id}` - View details of a single contact.

5\. Templates
-------------

HTML pages use Jinja2 templating engine to dynamically render data:

*   `index.html` - Lists all contacts in a table with action buttons.
*   `form.html` - Used for both creating and editing contacts. The form fields are pre-filled for edit mode.
*   `show.html` - Displays detailed contact information.
*   `404.html` - Error page shown if a contact is not found.
*   Partial templates for common page sections like `head.html` and `navbar.html`.

Form submissions use `POST` method with `action` URL changing based on context (create vs edit).

6\. Database Interaction
------------------------

Contacts are stored in MongoDB, accessed asynchronously via the `motor` driver.

*   `ContactModel` defines fields like first name, last name, email, phone, and address.
*   CRUD operations are defined in `contact_controller.py` and include:

*   `get_all_contacts(db)`
*   `get_contact_by_id(db, id)`
*   `create_contact(db, contact)`
*   `update_contact(db, id, contact)`
*   `delete_contact(db, id)`

*   Routes call these controller functions and pass the database instance from the FastAPI app state.

7\. How Data Is Passed to Templates
-----------------------------------

Data is sent to templates using `TemplateResponse` with a dictionary of variables:

    return templates.TemplateResponse("index.html", {
        "request": request,
        "contacts": contacts_list
    })
    

The `request` object is always passed for Jinja2 compatibility, and additional data like `contacts` is passed for rendering.

8\. Running the Project
-----------------------

Start the FastAPI server with:

    uvicorn main:app --reload

Open your browser and visit [/contacts](http://127.0.0.1:8000/contacts) to see the contact list.

Use the "Add New" button to create contacts, edit or delete existing ones.

9\. Notes
---------

*   Make sure MongoDB is running and accessible.
*   Use Python 3.8+ for compatibility.
*   Use virtual environments to isolate dependencies.
*   The project uses asynchronous functions to keep performance efficient.
*   Bootstrap and FontAwesome CDN links are included for UI styling and icons.

10\. Commands Summary
---------------------

    # Clone the repo
    git clone <repo-url>
    
    # Create and activate virtual environment (Linux/macOS)
    python3 -m venv venv
    source venv/bin/activate
    
    # Windows PowerShell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    
    # Install dependencies
    pip install fastapi uvicorn motor jinja2
    
    # Run the server
    uvicorn main:app --reload
    

© 2025 Contact App by Your Name