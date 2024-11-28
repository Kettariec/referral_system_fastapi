from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List


class ReferralCodeCreateResponse(BaseModel):
    code: str
    expires_at: datetime

    class Config:
        orm_mode = True


class ReferralCodeByEmailResponse(BaseModel):
    code: str
    expires_at: datetime

    class Config:
        orm_mode = True


class ReferralUserResponse(BaseModel):
    id: int
    email: EmailStr
    is_email_verified: bool

    class Config:
        orm_mode = True


class GetReferralsResponse(BaseModel):
    referrals: List[ReferralUserResponse]

    class Config:
        orm_mode = True
