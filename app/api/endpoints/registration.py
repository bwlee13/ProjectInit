from loguru import logger
from utils import db_utils
from fastapi import  APIRouter, HTTPException, Response
from app.api.models.registration import NewUser

router = APIRouter()


@router.get("/test")
async def test():
    return {"message": "test"}


@router.post('/', status_code=200)
async def  signup(data: NewUser):
    first_name = data.firstName
    last_name = data.lastName
    login_id = data.loginID
    email = data.email

    return ("You signed up with: ", first_name, last_name, login_id, email)

