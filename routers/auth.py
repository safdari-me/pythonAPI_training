from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(
            #توی http exception نباید به یوزر بگیم که پسوردت اشتباهه
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )
    # create token

    access_token = oauth2.create_access_token(data={"user_id":user.id})

    # return token

    return {"access_token":access_token, "token_type":"bearer"} 