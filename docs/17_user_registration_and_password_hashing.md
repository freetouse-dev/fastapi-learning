# 17. User Authentication & Security (Part 1: Password Hashing & Registration)

A quick reference and revision guide for password hashing using bcrypt, Pydantic email validation, and the user registration flow.

---

## 1. What Did We Do?
We created the foundation of our user management system:
1. Installed `bcrypt` (cryptographic hashing) and `pydantic[email]` (`EmailStr` validation).
2. Created `security.py` with `hash_password()` and `verify_password()`.
3. Created the `User` database model in `models/user.py`.
4. Created `UserCreate` and `UserResponse` in `schemas/user.py`.
5. Created `POST /auth/register` in `routers/auth.py`.

---

## 2. Why Did We Do It?
- **One-Way Cryptographic Hashing**: Passwords must **never** be stored in plain text. `bcrypt` generates a unique random salt for every password and uses adaptive hashing, making brute-force and rainbow table attacks computationally infeasible.
- **Strict Separation of Input vs Output**:
  - `UserCreate` takes the incoming plain `password`.
  - `UserResponse` **omits the password entirely**, guaranteeing the server never leaks hashes back to clients.
- **Email Normalization & Validation**: `EmailStr` ensures bad email strings like `"user@@domain"` are stopped by Pydantic before reaching the database.

---

## 3. How Does It Work?

```
Client sends { "email": "ajay@example.com", "password": "securepassword" }
                               │
                               ▼
              Pydantic validates types & email format
                               │
                               ▼
        Check if user with this email already exists in DB
              (If exists ➔ 400 Bad Request)
                               │
                               ▼
   hash_password("securepassword") ➔ "$2b$12$eX4mP1E..."
                               │
                               ▼
   Save User(email=..., hashed_password=...) into database
                               │
                               ▼
  Return UserResponse (id, email, is_active) with 201 Created
```

### Key Security Code (`security.py`):
```python
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
```
- `gensalt()`: Generates a random cryptographic salt so two users with the identical password will have completely different hashes.
- `checkpw()`: Compares the incoming plain password against the stored hash in constant time to prevent timing attacks.
