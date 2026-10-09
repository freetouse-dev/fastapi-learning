# 18. JWT Authentication & OAuth2 Password Bearer

A quick reference and revision guide for stateless token authentication using JSON Web Tokens (JWT) and FastAPI's `OAuth2PasswordBearer`.

---

## 1. What Did We Do?
We implemented full JWT-based authentication:
1. Installed `pyjwt` with `uv add pyjwt`.
2. Configured `SECRET_KEY`, `ALGORITHM` (HS256), and `ACCESS_TOKEN_EXPIRE_MINUTES` in `config.py`.
3. Created `create_access_token()` to cryptographically sign tokens containing user claims (`sub`) and expiration (`exp`).
4. Created `POST /auth/login` accepting `OAuth2PasswordRequestForm` and returning `{ "access_token": "...", "token_type": "bearer" }`.
5. Created the `get_current_user` dependency to protect routes and inject the authenticated `User` object.
6. Created `GET /auth/me` as our first protected endpoint.

---

## 2. Why Did We Do It?
- **Stateless & Scalable**: The server does not store active sessions in RAM or a session database. Every incoming token contains cryptographically verified claims.
- **Industry Standard (OAuth2 & Bearer Tokens)**: Compatible with web apps, mobile apps, and third-party API clients.
- **Built-in Swagger UI Integration**: `OAuth2PasswordBearer` automatically activates the green **"Authorize 🔓"** button in `/docs`.

---

## 3. How Does It Work?

### A. The JWT Lifecycle:
```
1. Login Request: POST /auth/login (username/email + password)
                      │
                      ▼
2. Server verifies password using verify_password()
                      │
                      ▼
3. Server generates JWT signed with SECRET_KEY:
   Payload: { "sub": "ajay@example.com", "exp": <timestamp> }
                      │
                      ▼
4. Client stores access_token and includes it in subsequent requests:
   Header: Authorization: Bearer <access_token>
                      │
                      ▼
5. get_current_user dependency:
   - Reads token from Authorization header
   - Validates cryptographic signature using SECRET_KEY
   - Checks expiration time ("exp")
   - Loads User from SQLite and injects into the route
```

### B. Core Security Code (`security.py`):
```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
```

---

## 4. How to Protect Any Endpoint in FastAPI

To require authentication on any endpoint in your entire API, simply inject `current_user: User = Depends(get_current_user)`:

```python
@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.email}!"}
```
If the token is missing, expired, or tampered with, FastAPI automatically rejects the request with **`401 Unauthorized`** before your route function ever runs.
