from fastapi import APIRouter,HTTPException
from fastapi.responses import StreamingResponse
from influxdb_client.client.write_api import SYNCHRONOUS
from domain import *
from config import (
    URL,TOKEN,ORG,BROKER,PORT,TOPIC,CLIENT_ID,MQTT_USERNAME,MQTT_PASSWORD,TELEGRAF
)

Influx = InfluxDataBase(URL,TOKEN,ORG)
router = APIRouter(      
    prefix="/api/v1/content",
    responses={ 
        404 : {
            'message': 'Not Found'
        }
    }
)
@router.get("/read/latest")
async def test():
    try:
        return Influx.read_data_latest()
    except:
        raise HTTPException(status_code=404, detail="Something has problem")
    
@router.get("/")
async def test1():
    try:
        return "complete system eiei"
    except:
        raise HTTPException(status_code=404, detail="Something has problem")

@router.get("/test")
async def test2():
    return "complete system"
