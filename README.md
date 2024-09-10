# Company Asset Management API

This project is a **Company Asset Management API** built using **FastAPI** and **PostgreSQL**. 
It allows companies to manage their assets, assign them to employees, and track their usage.
The application also includes a role-based authentication system with different user types (Super Admin, Company Admin).

## Features

- **Company Management**: 
  - Sign up as a company.
  - Company details can be added, updated, retrieved, or deleted.
  - Super Admin can approve or reject company sign-up requests.

- **Asset Management**:
  - Add, update, retrieve, and delete assets.
  - Assign assets to employees and track assignment status.
  
- **Authentication and Authorization**:
  - JWT-based authentication.
  - Role-based access control (Super Admin, Company Admin).

- **Employee Management**:
  - Add, update, and manage employees for each company.
  - Role-based access to different endpoints.

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ashik-creates/company_app.git
    cd company_app
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file with the following environment variables:

    ```
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=postgres
    DB_PASSWORD=your_password
    DB_NAME=company_app

    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60

    SUPER_ADMIN_EMAIL=your_email
    SUPER_ADMIN_PASSWORD=your_password
    SUPER_ADMIN_NAME=SuperAdmin
    ```

5. Run database migrations:

    ```bash
    alembic upgrade head
    ```

6. Start the application:

    ```bash
    uvicorn main:app --reload
    ```

7. The API will be available at `http://127.0.0.1:8000` or `http://127.0.0.1:8000/docs`.

### Creating a Super Admin

On the first run, if there is no Super Admin in the database, one will be automatically created using the values provided in the environment variables. 

Make sure to customize the `.env` file with the credentials you want for the Super Admin.

## API Endpoints

### Authentication

- **Login**: `/login` - Authenticate with your credentials and receive a JWT token.

### Companies

- **GET** `/companies/` - Retrieve all companies.
- **GET** `/companies/{company_id}` - Retrieve one company.
- **PUT** `/companies/{company_id}` - Update a company's information.
- **DELETE** `/companies/{company_id}` - Delete a company (Super Admin or the company's own admin only).

### Company Signup
- **POST** `/companies/` - Signup for new company.
- **GET** `/companies/pending/all` - Retrieve all pending company (Only for Super Admin).
- **POST** `/companies/{company_id}/approve` - Approve a pending company (Only for Super Admin). 
- **DELETE** `/companies/{company_id}/reject` - Reject a pending company (Only for Super Admin).

### Employees

- **GET** `companies/{company_id}/employees` - Retrieve all employees for the current company.
- **POST** `companies/{company_id}/employees` - Add an employee to the current company.
- **GET** `/employees/{id}` - Retrieve an employee of the current company.
- **PUT** `/employees/{id}` - Update an employee of the current company.
- **DELETE** `/employees/{id}` - Delete an employee of the current company.

### Assets

- **GET** `companies/{company_id}/assets` - Retrieve all assets for the current company.
- **POST** `companies/{company_id}/assets` - Add a new asset to the current company.
- **GET** `/assets/{asset_id}` - Retrieve an asset.
- **PUT** `/assets/{asset_id}` - Update an asset.
- **DELETE** `/assets/{asset_id}` - Delete an asset.




### Asset Assignments

- **POST** `assets/{id}/assign` - Assign an asset to an employee.
- **POST** `assets/{id}/unassign` - Unassign an asset to an employee.
- **GET** `assets/{id}/assignments` - Get assignments.
- **GET** `assets/{id}/history` - Get asset histroy.

## Middleware

CORS middleware is set up to allow requests from any origin. Modify the CORS settings in `main.py` as needed.

## License

This project is licensed under the MIT License.
