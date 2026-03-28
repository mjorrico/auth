from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
import logging

from app.modules.postgredb import db
from app.modules.auth_tools import (
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user_token,
    require_capability,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["auth"])


class LoginRequest(BaseModel):
    email: EmailStr = "verified@jordanenrico.com"
    password: str = "SecretPassword"


@router.get("/protected-resource")
async def protected_resource(payload: dict = Depends(get_current_user_token)):
    return {
        "message": "This is a protected resource",
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
    }


@router.get("/check-create-user")
async def check_create_user(
    user_data: dict = Depends(require_capability("user:create")),
):
    logger.info(f"Payload: {payload}")
    return


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
        data={
            "sub": str(user["id"]),
            "email": user["email"],
        }
    )
    refresh_token = create_refresh_token(
        data={
            "sub": str(
                user["id"],
            )
        }
    )

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
