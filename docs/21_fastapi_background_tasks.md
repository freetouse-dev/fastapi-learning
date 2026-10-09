# 21. FastAPI Background Tasks (`BackgroundTasks`)

A quick reference and revision guide for executing non-blocking background jobs after sending HTTP responses.

---

## 1. What Did We Do?
We integrated FastAPI's built-in `BackgroundTasks` into our user registration endpoint:
1. Created a worker function `send_welcome_email(email: str)` that simulates external network I/O.
2. Injected `background_tasks: BackgroundTasks` into `POST /auth/register`.
3. Queued the task using `background_tasks.add_task(send_welcome_email, new_user.email)`.
4. The client receives the `201 Created` HTTP response immediately, while the email job executes in the background.

---

## 2. Why Did We Do It?
- **Instant Client Response**: Prevents frontend and mobile users from experiencing lag while third-party operations (emails, webhooks, analytics) complete.
- **Simplicity**: For lightweight post-request tasks, you do not need heavy distributed message queues (like Celery, Redis Queue, or RabbitMQ).
- **Graceful Error Isolation**: If an external email provider fails or times out in the background task, the user's registration still succeeded and the HTTP request was not broken.

---

## 3. How Does It Work?

```
Client sends POST /auth/register
                │
                ▼
Route handler saves User to database
                │
                ▼
background_tasks.add_task(func, arg1, arg2...)
                │
                ▼
FastAPI returns HTTP 201 Created to Client (Response Complete)
                │
                ▼
FastAPI automatically executes queued background tasks
```

### Code Implementation:
```python
from fastapi import BackgroundTasks

def send_welcome_email(email: str):
    time.sleep(3)  # Simulates sending an email
    print(f"✅ Email sent to {email}")

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    ...
    # Schedules function to run after HTTP response is sent:
    background_tasks.add_task(send_welcome_email, new_user.email)
    
    return new_user
```

---

## 4. `BackgroundTasks` vs Distributed Queues (Celery / Redis)

| Feature | FastAPI `BackgroundTasks` | Celery / Redis Queue (ARQ, RQ) |
| :--- | :--- | :--- |
| **Setup** | Zero setup; built into FastAPI | Requires Redis/RabbitMQ + worker processes |
| **Persistence** | In-memory (tasks lost if server crashes) | Persistent; jobs survive server crashes |
| **Retries** | Manual try/catch | Built-in automatic retries with exponential backoff |
| **Best For** | Sending emails, audit logging, lightweight tasks | Video encoding, long data pipelines, heavy CPU jobs |
