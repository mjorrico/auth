from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

from app.modules.postgredb import db
from app.modules.auth_tools import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_access_token,
)

router = APIRouter(tags=["auth"])
security = HTTPBearer()


class LoginRequest(BaseModel):
    email: EmailStr = "verified@jordanenrico.com"
    password: str = "SecretPassword"


async def get_current_user_token(
    auth: HTTPAuthorizationCredentials = Depends(security),
):
    payload = verify_access_token(auth.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


@router.get("/protected-resource")
async def protected_resource(payload: dict = Depends(get_current_user_token)):
    return {
        "message": "This is a protected resource",
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
    }


@router.post("/login")
async def login(login_data: LoginRequest):
    with db.transaction() as cur:
        cur.execute(
            "SELECT id, email, password_hash, is_verified, is_banned FROM users WHERE email = %s",
            (login_data.email,),
        )
        user = cur.fetchone()

    if (
        not user
        or not verify_password(user["password_hash"], login_data.password)
        or user["is_banned"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user["is_verified"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not verified"
        )

    access_token = create_access_token(
        data={"sub": str(user["id"]), "email": user["email"]}
    )
    refresh_token = create_refresh_token(data={"sub": str(user["id"])})

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": str(user["id"]),
        "email": user["email"],
    }


@router.post("/refresh")
def refresh_token():
    pass
