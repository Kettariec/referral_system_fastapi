from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_email_verified = Column(Boolean, default=False)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    referrals = relationship("User", backref="referrer", remote_side=[id])
    referral_code = relationship("ReferralCode", back_populates="user", uselist=False)

    def __str__(self):
        return f'User {self.email}'
