from app.db.client import db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(name: str, email: str, password: str):
    if db.users.find_one({"email": email}):
        raise ValueError("User already exists")

    hashed_password = pwd_context.hash(password)

    result = db.users.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password
    })

    return {
        "id": str(result.inserted_id),
        "name": name,
        "email": email
    }

def authenticate_user(email: str, password: str):
    user = db.users.find_one({"email": email})
    if not user:
        return None

    if not pwd_context.verify(password, user["password"]):
        return None

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }
