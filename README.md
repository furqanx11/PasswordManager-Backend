# PasswordManager-Backend

## Overview
PasswordManager-Backend is a secure and efficient backend service to manage credentials and other fields for various services essential to your project workflow. It is built using **FastAPI** and **Tortoise ORM**, providing a robust and scalable solution for handling authentication, authorization, and role-based access control (RBAC).

## Features
- **Secure Credential Storage**: Safely stores fields and credentials.
- **Role-Based Access Control (RBAC)**: Fine-grained access control for users and their roles.
- **Authentication**: User authentication via secure password hashing.
- **FastAPI**: High-performance asynchronous backend.
- **PostgreSQL**: Relational database for storing sensitive data.

## Security
- **Sensitive keys** are encrypted using **RSA** before being stored in the database. The RSA encryption process uses a **1024-bit key size** to generate both public and private keys.
- Encryption utilizes **Optimal Asymmetric Encryption Padding (OAEP)** with **SHA-256** as the hashing algorithm. This combination ensures the confidentiality and integrity of the data, making it highly secure and resistant to attacks.
- Encrypted keys are stored in the database as **base64-encoded strings**. This encoding ensures that the ciphertext remains safe during transmission and storage.
- For decryption, the system uses the **private RSA key** along with **SHA-256 padding** to securely retrieve the original sensitive information for authorized users.

## Entity-Relationship Diagram
![ERD](images/erd_image.png)

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL

### Setup Instructions

1. **Clone the Repository**
2. **Install Required Libraries Install dependencies from requirements.txt**
   ```pip install -r requirements.txt```
3. **Create a .env file in the root of your project with your PostgreSQL credentials:**
   ```DATABASE_URL="postgres://username:password@localhost/db_name"```
4. **Run the Application Start the FastAPI server with Uvicorn:**
   ```uvicorn app.main:app --reload```
