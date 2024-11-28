from dao.base import BaseDAO
from database import async_session_maker
from datetime import datetime, timedelta
import random
from referral_system.model import ReferralCode
import string
from sqlalchemy import delete
from sqlalchemy.future import select
from users.model import User


class ReferralCodeDAO(BaseDAO):
    model = ReferralCode

    @classmethod
    async def generate_code(cls, user_id: int, expires_in_days: int) -> ReferralCode:
        async with async_session_maker() as session:
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            referral_code = ReferralCode(
                user_id=user_id,
                code=code,
                is_active=True,
                expires_at=datetime.utcnow() + timedelta(days=expires_in_days),
            )
            session.add(referral_code)
            await session.commit()
            return referral_code

    @classmethod
    async def delete_code(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(ReferralCode).where(ReferralCode.user_id == user_id)
            result = await session.execute(query)
            referral_code = result.scalar_one_or_none()

            if not referral_code:
                raise ValueError("Active referral code not found for the user")

            # Удаляем код
            await session.execute(delete(ReferralCode).where(ReferralCode.id == referral_code.id))
            await session.commit()

            return referral_code

    @classmethod
    async def find_by_email(cls, email: str) -> ReferralCode:
        async with async_session_maker() as session:
            query = (
                select(ReferralCode)
                .join(User, User.id == ReferralCode.user_id)
                .filter(User.email == email)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_referrals(cls, referrer_id: int) -> list[User]:
        async with async_session_maker() as session:
            query = select(User).filter(User.referrer_id == referrer_id)
            result = await session.execute(query)
            return result.scalars().all()
