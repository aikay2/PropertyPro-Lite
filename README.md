# PropertyPro-Lite

**PropertyPro-Lite** is a platform where users can create, view, and manage property advertisements. This project implements the backend API for managing property listings, user authentication, and more using Django and Django Rest Framework (DRF). It also includes JWT-based authentication and user management via Djoser.

## Project Overview

This project fulfills **Challenge 2** of the Andela Developer Challenge using Django and Django Rest Framework. The key features implemented include user authentication, property advert creation, updates, filtering, and more. The API is documented using **Swagger**.

### Features Implemented:
1. User can sign up and log in.
2. User (agent) can post property adverts.
3. User (agent) can update details of a property advert.
4. User (agent) can mark a property as sold.
5. User can view all properties.
6. User can view properties of a specific type (e.g., 2-bedroom, 3-bedroom).
7. Users can flag property adverts for suspicious activities.

### Technologies Used:
- **Django**: Web framework for rapid development.
- **Django Rest Framework (DRF)**: To build APIs.
- **JWT (JSON Web Tokens)**: For secure token-based authentication.
- **Djoser**: Simplifies user authentication and management.
- **Swagger**: To document API endpoints.

---

## API Documentation

API documentation is accessible through **Swagger** at:
- `/docs/`: Swagger UI.
- `/redoc/`: ReDoc UI.
  
To view the Swagger documentation:
```bash
http://127.0.0.1:8000/docs/
```

## Project Setup

### Requirements:
- Python 3.7+
- Django 5.1+
- Django Rest Framework (DRF)
- Djoser
- drf-yasg (for Swagger documentation)
- SQLite (default database for local development)

### Installation Instructions:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aikay2/PropertyPro-Lite.git
   cd PropertyPro-Lite
   ```
2. **Set up a virtual environment**:
   ```bash
   pip install pipenv
   pipenv shell
   ```
3. **Install dependencies**:
   ```bash
   pipenv install
   ```
4. **Set up the database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```
7. **Access the admin panel**:
   ```bash
   http://127.0.0.1:8000/admin/
   ```

### Endpoints

#### User Authentication:
- **POST** `/auth/users/`: User sign-up.
- **POST** `/auth/jwt/create/`: Obtain a JWT token.
- **POST** `/auth/jwt/refresh/`: Refresh JWT token.
- **POST** `/auth/jwt/verify/`: Verify JWT token.

#### Property API:
- **GET** `/api/v1/property/`: Get all property adverts.
- **POST** `/api/v1/property/`: Create a property advert (Agents only).
- **GET** `/api/v1/property/<property_id>/`: Retrieve a single property advert.
- **PUT** `/api/v1/property/<property_id>/`: Update a property (Agents only).
- **PATCH** `/api/v1/property/<property_id>/sold/`: Mark a property as sold (Agents only).
- **DELETE** `/api/v1/property/<property_id>/`: Delete a property (Agents only).
- **POST** `/api/v1/property/<property_id>/flag/`: Flag a property advert.

#### Flags API:
- **GET** `/api/v1/property/flags/`: Get all flags.
- **GET** `/api/v1/property/<property_id>/flags/`: Get flags for a specific property.
- **GET** `/api/v1/property/flags/<flag_id>/`: Retrieve, update, or delete a flag.




