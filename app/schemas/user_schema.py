from pydantic import BaseModel
from typing import Optional

class CustomizationRequest(BaseModel):
    avatar: Optional[str] = None
    theme: Optional[str] = None
    pattern: Optional[str] = None
