from app.repositories.user_repo import get_user_by_email, create_user
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
import uuid


def register_user(db, email, password, role):
    existing = get_user_by_email(db, email)
    if existing:
        raise Exception("User already exists")

    user = User(
        id=str(uuid.uuid4()),
        email=email,
        password_hash=hash_password(password),
        role=role
    )

    return create_user(db, user)


def login_user(db, email, password):
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.password_hash):
        raise Exception("Invalid credentials")

    token = create_access_token({"sub": user.id, "role": user.role})
    return {"access_token": token}