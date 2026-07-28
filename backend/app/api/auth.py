import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import UserWorkspace
from pydantic import BaseModel, EmailStr

SECRET_KEY = "SUPER_SECRET_ZAR_STUDIO_KEY"
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    company_name: str

class TokenData(BaseModel):
    email: str | None = None

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate workspace session tokens.")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(UserWorkspace).filter(UserWorkspace.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register")
async def register_user(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(UserWorkspace).filter(UserWorkspace.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Workspace already configured.")
    new_workspace = UserWorkspace(email=user.email, password_hash=user.password, company_name=user.company_name, currency="ZAR")
    db.add(new_workspace)
    db.commit()
    db.refresh(new_workspace)
    return {"status": "success", "workspace_id": new_workspace.id}
