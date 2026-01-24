from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

from app.modules.postgredb import db
from app.modules.auth_tools import verify_password

router = APIRouter(tags=["auth"])
security = HTTPBearer()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.get("/print-token")
async def print_token(token: HTTPAuthorizationCredentials = Depends(security)):
    print(f"Bearer token: {token.credentials}")
    return {"token": token.credentials}


@router.post("/login")
async def login(login_data: LoginRequest):
    with db.transaction() as cur:
        cur.execute(
            "SELECT id, email, password_hash FROM users WHERE email = %s",
            (login_data.email,),
        )
        user = cur.fetchone()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not verify_password(user["password_hash"], login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    return {
        "message": "Login successful",
        "user_id": str(user["id"]),
        "email": user["email"],
    }
