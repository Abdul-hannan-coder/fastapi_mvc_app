# Contact Management App

A modern CRUD web application to manage contacts built with **FastAPI** (backend) and **Jinja2** templates (frontend). This project demonstrates MVC architecture principles with FastAPI, MongoDB integration, and responsive web design.

## 🚀 Features

- **Full CRUD Operations**: Create, Read, Update, Delete contacts
- **FastAPI Backend**: Async/await support with automatic API documentation
- **MongoDB Integration**: Asynchronous database operations using Motor
- **Responsive Design**: Bootstrap 4 for mobile-friendly UI
- **MVC Architecture**: Clean separation of concerns
- **Form Validation**: Pydantic models with email validation
- **Environment Configuration**: Secure database connection management

## 📁 Project Structure

```
fastapi_mvc_app/
├── main.py                     # FastAPI app entry point
├── server.py                   # Server configuration
├── controllers/
│   └── contact_controller.py   # Business logic for CRUD operations
├── models/
│   └── contact_model.py        # Pydantic data models
├── routes/
│   ├── contact_routes.py       # API routes for contacts
│   └── view_routes.py          # HTML view routes
├── views/                      # Jinja2 HTML templates
│   ├── index.html             # Contact list view
│   ├── form.html              # Create/Edit contact form
│   ├── show.html              # Contact details view
│   └── partials/
│       ├── head.html          # Common head section
│       └── navbar.html        # Navigation component
├── database/
│   └── database.py            # Database connection setup
├── utils/
│   └── helper.py              # Utility functions
└── pyproject.toml             # Project dependencies and metadata
```

## 🛠️ Installation and Setup

### Prerequisites
- Python 3.12 or higher
- MongoDB (local or cloud instance)
- UV package manager (recommended)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-github-repo-url>
   cd fastapi_mvc_app
   ```

2. **Install UV (if not already installed)**
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Install dependencies using UV**
   ```bash
   # Install all dependencies from pyproject.toml
   uv sync
   
   # Or add dependencies individually if needed
   uv add fastapi[all]
   uv add jinja2
   uv add motor
   uv add pydantic[email]
   uv add python-dotenv
   uv add uvicorn
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "MONGODB_URL=mongodb://localhost:27017" > .env
   echo "DATABASE_NAME=contact_app" >> .env
   ```

5. **Start the development server**
   ```bash
   # Using UV
   uv run uvicorn main:app --reload
   
   # Or activate virtual environment and run
   uv run python -m uvicorn main:app --reload
   ```

6. **Access the application**
   - Main application: http://127.0.0.1:8000/contacts
   - API documentation: http://127.0.0.1:8000/docs
   - Alternative API docs: http://127.0.0.1:8000/redoc

## 🔄 API Routes

- `GET /api/contacts` - List all contacts (JSON response)
- `GET /api/contacts/{contact_id}` - Get details of a specific contact
- `POST /api/contacts` - Create a new contact
- `PUT /api/contacts/{contact_id}` - Update an existing contact
- `DELETE /api/contacts/{contact_id}` - Delete a contact

## 🖥️ View Routes

- `GET /contacts` - List all contacts (HTML view)
- `GET /contacts/create` - Show form to create a new contact
- `POST /contacts/create` - Submit new contact data
- `GET /contacts/edit/{contact_id}` - Show form to edit an existing contact
- `POST /contacts/edit/{contact_id}` - Submit updated contact data
- `POST /contacts/delete/{contact_id}` - Delete a contact
- `GET /contacts/show/{contact_id}` - View contact details

## 🎨 Templates

HTML pages use Jinja2 templating engine to dynamically render data:

- `index.html` - Lists all contacts in a table with action buttons
- `form.html` - Used for both creating and editing contacts (fields pre-filled for edit mode)
- `show.html` - Displays detailed contact information
- Partial templates for common sections:
  - `partials/head.html` - Common HTML head section
  - `partials/navbar.html` - Navigation component

Form submissions use `POST` method with `action` URL changing based on context (create vs edit).

## 🗄️ Database Configuration

The application uses MongoDB as its database, with the connection managed through the Motor driver for asynchronous operations:

- `ContactModel` defines fields like first name, last name, email, phone, and address
- CRUD operations are defined in `contact_controller.py` and include:
  - `get_all_contacts(db)`
  - `get_contact_by_id(db, id)`
  - `create_contact(db, contact)`
  - `update_contact(db, id, contact)`
  - `delete_contact(db, id)`

- Routes call these controller functions and pass the database instance from the FastAPI app state

## 🔧 Development Notes

- Ensure MongoDB is running and accessible before starting the application
- The project requires Python 3.12+ for optimal compatibility
- Uses asynchronous functions throughout for efficient performance
- Bootstrap 4 and FontAwesome are used for responsive UI styling and icons
- Environment variables are used for secure database connection management

## 📋 Quick Commands Reference

```bash
# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup project
git clone <repo-url>
cd fastapi_mvc_app

# Install dependencies
uv sync

# Add new dependencies
uv add package_name

# Run development server
uv run uvicorn main:app --reload

# Run with custom host and port
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```


## 🚢 Deployment

### Docker Deployment

1. **Build the Docker image**
   ```bash
   # Create Dockerfile if not exists
   # Build the image
   docker build -t fastapi-contact-app .
   ```

2. **Run with Docker Compose**
   ```bash
   # Start all services (app + MongoDB)
   docker-compose up -d
   ```

### Nginx Reverse Proxy Setup

For production deployment, configure Nginx as a reverse proxy:

1. **Create Nginx configuration directory**
   ```bash
   mkdir -p ~/nginx/conf.d
   ```

2. **Create Nginx configuration file**
   ```bash
   nano ~/nginx/conf.d/fastapi.conf
   ```

3. **Add the following configuration**
   ```nginx
   server {
       listen 80;
       server_name your-domain-or-ip;
   
       location / {
           proxy_pass http://app:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. **Run Nginx container**
   ```bash
   docker run -d \
     --name nginx-proxy \
     --network fastapi_mvc_app_app-network \
     -p 80:80 \
     -v ~/nginx/conf.d:/etc/nginx/conf.d:ro \
     nginx:latest
   ```

5. **Verify deployment**
   ```bash
   # Check running containers
   docker ps
   
   # Test application
   curl http://your-server-ip/contacts
   ```

## 🔒 Production Considerations

### SSL/HTTPS Setup

For production deployment with SSL:

1. **Obtain a domain name** and configure DNS A record
2. **Open port 443** in your firewall/security groups
3. **Use Let's Encrypt for SSL certificates**:
   ```bash
   # Install certbot
   sudo apt install certbot python3-certbot-nginx
   
   # Obtain certificate
   sudo certbot --nginx -d your-domain.com
   ```
4. **Update Nginx configuration** to include SSL settings

### Security Best Practices

- Use environment variables for sensitive configuration
- Enable CORS properly for production
- Implement rate limiting
- Regular security updates for dependencies
- Use secrets management for database credentials
- Enable MongoDB authentication in production

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Contact search and filtering capabilities
- [ ] Export contacts to CSV/Excel
- [ ] Contact categories and tags
- [ ] API rate limiting and caching
- [ ] Mobile-responsive Progressive Web App (PWA)
- [ ] Contact import functionality
- [ ] Advanced contact validation
- [ ] Contact history and audit trail
- [ ] Email integration for contact communication

---

© 2025 FastAPI Contact Management App
