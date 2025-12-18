from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta
import json

from ..db.session import get_db
from ..utils.auth import (
    Token,
    UserRegistration,
    authenticate_user,
    create_access_token,
    create_user,
    get_user_by_email
)
from ..db.models import User

router = APIRouter(prefix="/better-auth", tags=["better-auth"])

# HTTP Bearer token for authentication
security = HTTPBearer()


@router.post("/sign-up")
async def better_auth_sign_up(
    request: Request,
    db: Session = Depends(get_db)
):
    """Better-Auth compatible sign up endpoint."""
    try:
        body = await request.json()
        email = body.get("email")
        password = body.get("password")
        name = body.get("name", "")

        # Extract background information
        software_background = body.get("software_background", "")
        hardware_background = body.get("hardware_background", "")
        experience_level = body.get("experience_level", "")

        # Check if user already exists
        existing_user = get_user_by_email(db, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user with background information
        user_data = UserRegistration(
            email=email,
            password=password,
            full_name=name,
            software_background=software_background,
            hardware_background=hardware_background,
            experience_level=experience_level
        )

        db_user = create_user(db, user_data)

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": db_user.email}, expires_delta=access_token_expires
        )

        return {
            "user": {
                "id": str(db_user.id),
                "email": db_user.email,
                "name": db_user.full_name,
                "createdAt": db_user.created_at.isoformat() if db_user.created_at else None,
                "software_background": db_user.software_background,
                "hardware_background": db_user.hardware_background,
                "experience_level": db_user.experience_level
            },
            "session": {
                "accessToken": access_token,
                "tokenType": "Bearer",
                "expiresAt": (db_user.created_at + access_token_expires).isoformat() if db_user.created_at else None
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/sign-in")
async def better_auth_sign_in(
    request: Request,
    db: Session = Depends(get_db)
):
    """Better-Auth compatible sign in endpoint."""
    try:
        body = await request.json()
        email = body.get("email")
        password = body.get("password")

        user = authenticate_user(db, email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return {
            "user": {
                "id": str(user.id),
                "email": user.email,
                "name": user.full_name,
                "createdAt": user.created_at.isoformat() if user.created_at else None,
                "software_background": user.software_background,
                "hardware_background": user.hardware_background,
                "experience_level": user.experience_level
            },
            "session": {
                "accessToken": access_token,
                "tokenType": "Bearer",
                "expiresAt": (user.created_at + access_token_expires).isoformat() if user.created_at else None
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/sign-out")
async def better_auth_sign_out():
    """Better-Auth compatible sign out endpoint."""
    return {"success": True}


@router.get("/session")
async def better_auth_session(
    token: str = Depends(security),
    db: Session = Depends(get_db)
):
    """Better-Auth compatible session endpoint."""
    from ..utils.auth import get_current_user_from_token

    user = get_current_user_from_token(db, token.credentials)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.full_name,
            "createdAt": user.created_at.isoformat() if user.created_at else None,
            "software_background": user.software_background,
            "hardware_background": user.hardware_background,
            "experience_level": user.experience_level
        },
        "session": {
            "accessToken": token.credentials,
            "tokenType": "Bearer",
            "expiresAt": None  # This would need to be calculated based on token expiry
        }
    }