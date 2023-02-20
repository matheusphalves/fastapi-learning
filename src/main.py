from fastapi import FastAPI
from src.resource.finance.financial_user.router import financial_user_router

app = FastAPI()

app.include_router(financial_user_router)


@app.get("/")
async def root():
    return {"message": "Hello world!"}
