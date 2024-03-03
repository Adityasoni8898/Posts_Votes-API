from pydantic import BaseModel, EmailStr
import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
import datetime
from typing import Optional


class BasePost(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

    
class PostCreate(BasePost):
    pass


class Post(BasePost):
    id: int
    created_at: datetime.datetime  # Use datetime.datetime instead of datetime
    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime  # Use datetime.datetime instead of datetime
    
    class Config:
        from_attributes = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]