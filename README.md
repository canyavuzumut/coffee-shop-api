# Coffee Shop API

This project is a RESTful API built with FastAPI, designed to meet the operational needs of a coffee shop. The application provides a secure way to manage coffee inventory, sales, and recipes using a role-based access control (RBAC) system.

## Features

* **Role-Based Access Control:** The system includes two distinct user roles: `manager` and `employee`.
* **Secure Authentication:** Utilizes JWT (JSON Web Token) for secure user login and session management.
* **Inventory Management:** Functionality to manage, update, and track coffee bean and milk stock.
* **Recipe Management:** Defines the required ingredient quantities (grams of coffee, ml of milk) for each coffee type.
* **Sales Transactions:** Processes sales by deducting the ingredients from stock based on the recipe and records the transaction.
* **Reporting:** Generates sales reports for daily, weekly, or specific date ranges.

## Setup and Running

1.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```
2.  **Activate the Virtual Environment:**
    * macOS / Linux:
        ```bash
        source venv/bin/activate
        ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (If `requirements.txt` does not exist, you can create it with `pip freeze > requirements.txt`.)
4.  **Create Database and Users:**
    ```bash
    python create_users.py
    ```
5.  **Start the API:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be running at `http://127.0.0.1:8000`.

## API Endpoints

You can find all API endpoints and detailed usage information on the Swagger UI interface: `http://127.0.0.1:8000/docs`

### Login

Use the `POST /login` endpoint to get an authentication token.

* **Manager:** `username: yonetici`, `password: sifre123`
* **Employee:** `username: calisan`, `password: sifre123`
