from pydantic import BaseModel, EmailStr
from pydantic.types import conint
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

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime  # Use datetime.datetime instead of datetime
    
    class Config:
        from_attributes = True


class Post(BasePost):
    id: int
    created_at: datetime.datetime  # Use datetime.datetime instead of datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        from_attributes = True
    
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]
    
class Vote(BaseModel):
    post_id: int
    direction: conint(le=1) # type: ignore