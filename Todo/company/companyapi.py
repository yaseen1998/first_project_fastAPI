from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_company_name():
    return {"company": "Todo"}


@router.get('/eployees')
async def number_of_employees():
    return {"employees": "100"}