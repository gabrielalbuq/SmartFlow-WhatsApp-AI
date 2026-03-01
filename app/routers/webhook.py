#Unica e exclusiva rota que vai receber todo e qualquer evento

from fastapi import APIRouter, BackgroundTasks, status

router = APIRouter()

@router.post("/webhook", status_code=status.HTTP_200_OK)
async def receive_webhook(data: dict, background_tasks: BackgroundTasks):
    """
    Endpoint que recebe os dados do webhook e processa em background
    """
    try:
        print(data)
    except Exception as ex:
        print(f"ERROR: {ex}")
        return {"message": "Error"}