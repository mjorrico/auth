from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.modules.auth_tools import verify_access_token
from app.modules.postgredb import db

security = HTTPBearer()


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


def require_capability(capability_id: str):
    async def capability_checker(payload=Depends(get_current_user_token)):
        user_id = payload.get("sub")
        with db.transaction() as cur:
            cur.execute(
                """
                SELECT u.id, u.role, c.name as capability_name
                FROM users u
                JOIN roles r ON u.role = r.id
                JOIN role_capabilities rc ON r.id = rc.role_id
                JOIN capabilities c ON rc.capability_id = c.id
                WHERE u.id = %s AND c.name = %s
                """,
                (user_id, capability_id),
            )
            row = cur.fetchone()
        print(f"Row: {row}")
        if not row:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )
        return dict(row)

    return capability_checker
