from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from referral_system.cache import cache_referral_code, redis_client
from referral_system.dao import ReferralCodeDAO
from referral_system.scheme import (ReferralCodeCreateResponse, ReferralCodeByEmailResponse,
                                    GetReferralsResponse, ReferralUserResponse)
from users.dependencies import get_current_user
from users.model import User

router = APIRouter(
    prefix="/referrals",
    tags=["Referrals"]
)


@router.post("/create", response_model=ReferralCodeCreateResponse)
async def create_referral_code(expires_in_days: int, current_user: User = Depends(get_current_user)):
    if expires_in_days <= 0:
        raise HTTPException(status_code=400, detail="Invalid expiration period")

    referral_code = await ReferralCodeDAO.generate_code(user_id=current_user.id, expires_in_days=expires_in_days)

    ttl = expires_in_days * 86400
    await cache_referral_code(referral_code.code,
                              {"code": referral_code.code, "expires_at": referral_code.expires_at.isoformat()}, ttl)

    return ReferralCodeCreateResponse(code=referral_code.code, expires_at=referral_code.expires_at)


@router.delete("/delete")
async def delete_referral_code(current_user: User = Depends(get_current_user)):
    try:
        referral_code = await ReferralCodeDAO.delete_code(user_id=current_user.id)
        await redis_client.delete(referral_code.code)
        return {"detail": f"Referral code '{referral_code.code}' deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/get-by-email", response_model=ReferralCodeByEmailResponse)
async def get_referral_code_by_email(email: str):
    referral_code = await ReferralCodeDAO.find_by_email(email=email)
    if not referral_code or not referral_code.is_active or referral_code.expires_at < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Referral code not found or expired")

    return ReferralCodeByEmailResponse(code=referral_code.code, expires_at=referral_code.expires_at)


@router.get("/my", response_model=GetReferralsResponse)
async def get_referrals(current_user: User = Depends(get_current_user)):
    referrals = await ReferralCodeDAO.find_referrals(referrer_id=current_user.id)
    return GetReferralsResponse(referrals=[ReferralUserResponse(id=ref.id, email=ref.email, is_email_verified=ref.is_email_verified) for ref in referrals])
