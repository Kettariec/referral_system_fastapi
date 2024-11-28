from fastapi import FastAPI
from referral_system.router import router as router_referral
from users.router import router as router_user

app = FastAPI()

app.include_router(router_user)
app.include_router(router_referral)
