# Pharmacy POS Backend

A modular backend for a Pharmacy/Chemist Point of Sale (POS) system. Built using **FastAPI** and **SQLAlchemy**, it handles over-the-counter sales alongside prescription-only checkout blocks and drug expiration tracking.

## Features

- **Pharmacy Validation**: Restricts regulated drug sales without a prescription and logs expiry dates for tablets, syrups, and capsules.
- **Modular Directory Structure**: Organized cleanly across Models, Repositories, Schemas, Services, and Routers.
- **Relational Tracking**: Full database mapping across Categories, Suppliers, Customers, Sales, Sale Items, Payments, and Receipts.
- **Auto-Generated Tables**: Automatically creates necessary database tables on application startup.



## Project Structure

The project follows a standard layered architecture:

- **`models/`**: Database models defined via SQLAlchemy ORM.
- **`repositories/`**: CRUD operations interacting directly with the database.
- **`schemas/`**: Request and response data structures managed by Pydantic v2.
- **`services/`**: Core business logic, error checks, and workflow rules.
- **`routers/`**: HTTP endpoints exposing API paths.

├── database.py         # Database connection and session engine
├── main.py             # FastAPI app configuration and router initialization
├── models/             # SQLAlchemy ORM models
├── repositories/       # Direct database query layers
├── routers/            # API endpoints
├── schemas/            # Request and response models
└── services/           # Business logic checks and exceptions


## Database Relationships

1. **Category Product** *(One-to-Many)*: Organizes items into explicit groups.
2. **Supplier Product** *(One-to-Many)*: Connects stock inventory to specific suppliers.
3. **Customer Sale** *(One-to-Many)*: Tracks transaction histories under individual customer profiles.
4. **User Sale** *(One-to-Many)*: Records which staff user processed a specific transaction.
5. **Sale Sale Item** *(One-to-Many)*: Breaks down line items belonging to a purchase.
6. **Product Sale Item** *(One-to-Many)*: Maps a single inventory product across different sales over time.
7. **Sale Payment** *(One-to-One)*: Links a finalized ticket directly to its payment details.
8. **Sale Receipt** *(One-to-One)*: Automatically issues a unique receipt document for every successful checkout.



## Local Setup

### Prerequisites
- Python 3.10+
- Virtual Environment tool (`venv`)

### 1. Installation
```bash
git clone https://github.com
cd pharmacy-pos-backend

# Set up and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic
```

### 2. Run the App
The database defaults to a local SQLite instance (`pharmacy_pos.db`). Launch the server using:
```bash
uvicorn main:app --reload
```


## API Documentation

When the local server is running, you can explore, test, and view the raw payload shapes via the automated docs:

- **Swagger UI**: [http://127.0.0](http://127.0.0)
- **ReDoc Dashboard**: [http://127.0.0](http://127.0.0)



## Endpoints Summary

| Module | Base Path | Methods |
| :--- | :--- | :--- |
| **Users** | `/users` | `GET`, `POST`, `PUT`, `DELETE` |
| **Categories** | `/categories` | `GET`, `POST`, `PUT`, `DELETE` |
| **Suppliers** | `/suppliers` | `GET`, `POST`, `PUT`, `DELETE` |
| **Products** | `/products` | `GET`, `POST`, `PUT`, `DELETE` |
| **Customers** | `/customers` | `GET`, `POST`, `PUT`, `DELETE` |
| **Sales** | `/sales` | `GET`, `POST`, `PUT`, `DELETE` |
| **Sale Items** | `/sale-items` | `GET`, `POST`, `PUT`, `DELETE` |
| **Payments** | `/payments`  `GET`, `POST`, `PUT`, `DELETE` |
| **Receipts** | `/receipts` `GET`, `POST`, `PUT`, `DELETE` |
