# doesnt use anywhere yet but will be help ide to auto complete user fields
from typing import TypedDict

class UserModel(TypedDict):
    name: str
    email: str
    password: str  # hashed
    avatar: str
    age: int  # optional
