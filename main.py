from fastapi import FastAPI,HTTPException,APIRouter
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware
from influxDatabase import InfluxDataBase
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
from config import (
    URL,TOKEN,ORG,BROKER,PORT,TOPIC,CLIENT_ID,MQTT_USERNAME,MQTT_PASSWORD,TELEGRAF
)
app = FastAPI()
MOVIES_LIST = [{"name" : "TENET"}]

Influx = InfluxDataBase(URL,TOKEN,ORG)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/api/v1/content/read/latest")
async def test():
    try:
        return Influx.read_data_latest()
    except:
        raise HTTPException(status_code=404, detail="Something has problem")
    
@app.get("/")
async def test1():
    try:
        return "complete system eiei"
    except:
        raise HTTPException(status_code=404, detail="Something has problem")

@app.get("/test")
async def test2():
    return "complete system"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)