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


Nginx Configuration for FastAPI Application
===========================================

This document outlines the steps to configure Nginx as a reverse proxy for a containerized FastAPI application using Docker on a Ubuntu VM. The goal is to route public traffic to the application on a standard port (like 80) without exposing the application's internal port directly.

Prerequisites
-------------

*   A working Docker environment on an Oracle Cloud VM.
*   A Docker Compose file (\`docker-compose.yml\`) that defines and runs the FastAPI application and a MongoDB database.
*   The FastAPI application container is running and is part of a Docker network (e.g., \`fastapi\_mvc\_app\_app-network\`).
*   Port 80 is open in your Oracle Cloud VM's security list.

Step 1: Create the Nginx Configuration Directory
------------------------------------------------

First, create a directory on your VM to store the Nginx configuration file. This directory will be mounted into the Nginx container.

    mkdir -p ~/nginx/conf.d

Step 2: Create the Nginx Configuration File
-------------------------------------------

Using a text editor like `nano`, create a new file named `fastapi.conf` inside the directory you just created.

    nano ~/nginx/conf.d/fastapi.conf

Paste the following content into the file. Be sure to replace `158.180.30.111` with your VM's public IP address.

    server {
        listen 80;
        server_name 158.180.30.111; # Your VM's public IP address
    
        location / {
            # This points to the 'app' service within the 'app-network' (internal Docker DNS)
            proxy_pass http://app:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    

**Explanation of the Configuration:**

*   `listen 80;`: Nginx listens for incoming traffic on port 80 (standard HTTP).
*   `server_name 158.180.30.111;`: Nginx responds to requests made to your VM's public IP.
*   `location / { ... }`: This block handles all requests to the root path.
*   `proxy_pass http://app:8000;`: This is the most important line. It forwards the incoming request to the Docker service named "app" on its internal port "8000." The name "app" comes from your `docker-compose.yml` file.

Step 3: Run the Nginx Docker Container
--------------------------------------

Now, run the Nginx container, connecting it to the same network as your FastAPI app and mounting the configuration file. This command will start the container in detached mode (`-d`).

    docker run -d \
      --name nginx-proxy \
      --network fastapi_mvc_app_app-network \
      -p 80:80 \
      -v ~/nginx/conf.d:/etc/nginx/conf.d:ro \
      nginx:latest
    

**Explanation of the Command:**

*   `--name nginx-proxy`: Assigns a user-friendly name to the container.
*   `--network fastapi_mvc_app_app-network`: Connects the Nginx container to the same internal Docker network as your FastAPI app. This allows Nginx to communicate with your app using the service name "app."
*   `-p 80:80`: Maps port 80 of your host VM to port 80 of the Nginx container.
*   `-v ~/nginx/conf.d:/etc/nginx/conf.d:ro`: Mounts your local configuration directory into the container. The `:ro` means it is read-only, which is a good security practice.
*   `nginx:latest`: Specifies the Docker image to use.

Step 4: Verify the Setup
------------------------

Once the container is running, you can verify that all components are working as expected.

1.  Check that all containers are running:

    docker ps

3.  Open your web browser and navigate to your public IP address:

    http://158.180.30.111/

You should now see your FastAPI application's response, served through Nginx.

Future Goal: Adding SSL/HTTPS Configuration
-------------------------------------------

For a secure and professional deployment, the next step is to add SSL (HTTPS). This requires a domain name, as free certificates cannot be issued for raw IP addresses.

The high-level steps for this are:

1.  Purchase a domain name and point its "A" record to your VM's public IP.
2.  Open port 443 (HTTPS) in your Oracle Cloud VM's security rules.
3.  Use a tool like Certbot to obtain a free SSL certificate from Let's Encrypt for your domain.
4.  Update your Nginx configuration file to listen on port 443 and use the SSL certificate.
5.  Modify the Nginx Docker run command to also expose port 443 and mount the certificate directories.

* * *

End of Document.
    

© 2025 Contact App by Your Name
