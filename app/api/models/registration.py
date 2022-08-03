from pydantic import BaseModel, Field
from typing import Optional, List


class NewUser(BaseModel):
    firstName: str
    lastName: str
    userId: str
    email: str
    password: str
