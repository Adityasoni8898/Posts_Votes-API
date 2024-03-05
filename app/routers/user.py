from .. import schemas, models, utils
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    
    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id:int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        return user