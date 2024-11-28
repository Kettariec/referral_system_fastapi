from config import settings
from _datetime import datetime
from exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from fastapi import APIRouter, Response, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse
from jose import JWTError
import jwt
from referral_system.dao import ReferralCodeDAO
from tasks.tasks import registration_message
from users.auth import get_password_hash, authenticate_user, create_access_token
from users.dao import UserDAO
from users.scheme import SchemeUserAuth


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register_user(user_data: SchemeUserAuth,
                        background_tasks: BackgroundTasks,
                        referral_code: str = None):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)

    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(email=user_data.email, hashed_password=hashed_password)

    if referral_code:
        referral = await ReferralCodeDAO.find_one_or_none(code=referral_code, is_active=True)
        if referral and referral.expires_at > datetime.utcnow():
            new_user.referrer_id = referral.user_id
            await UserDAO.update_with_referral(new_user)

    background_tasks.add_task(registration_message, user_data.email)


@router.get("/verify-email")
async def verify_email(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        user = await UserDAO.find_one_or_none(email=email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_email_verified = True
        await UserDAO.update(user)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token or token has expired")


@router.post("/login")
async def login_user(response: Response, user_data: SchemeUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    if not user.is_email_verified:
        raise HTTPException(status_code=403, detail="Пожалуйста, подтвердите вашу электронную почту перед входом")
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")