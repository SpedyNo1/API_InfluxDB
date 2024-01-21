from fastapi import FastAPI,HTTPException,APIRouter
import uvicorn 
from influxDatabase import InfluxDataBase
#app = FastAPI()
MOVIES_LIST = [{"name" : "TENET"}]
app = APIRouter(      
    prefix="/api/v1/content",
    responses={ 
        404 : {
            'message': 'Not Found'
        }
    }
)
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
from config import (
    URL,TOKEN,ORG,BROKER,PORT,TOPIC,CLIENT_ID,MQTT_USERNAME,MQTT_PASSWORD,TELEGRAF
)
# bucket = "<my-bucket>"
# org = "hadyai-iot"
# token = "UeeDmS1TFY-oWgV9I_xH6nsR-Yeo7K1rZeX5zSVc3bwmi2_y9Tz403v7yLFNh3CFOLOTXa8GQ_MuNAhUJLJ2Vw=="
# # Store the URL of your InfluxDB instance
# url="https://us-east-1-1.aws.cloud2.influxdata.com"
# client = influxdb_client.InfluxDBClient(
#     url=url,
#     token=token,
#     org=org
# )
# # Query script
# query_api = client.query_api()
# query = 'from(bucket:"sensor")\
# |> range(start: -5m)\
# |> filter(fn:(r) => r._measurement == "mqtt_consumer")\
# |> filter(fn:(r) => r._field == "DO_value")'
# query = f'from(bucket: "sensor")'  
# query += f'|> range(start: -1m)'
# query += f'|> filter(fn:(r) => r["_measurement"] == "mqtt_consumer")'
# query += f'|> filter(fn:(r) => r["_field"] == "DO_value")'
# #query=query+f'|> filter(fn: (r) => r["topic"] == "sgm/1703407002")'
# result = query_api.query(org=org, query=query)
# results = []
# for table in result:
#     for record in table.records:
#         results.append({"time":record.get_time(),"field":record.get_field(),"value":record.get_value(),"topic":record.values.get("topic")})
# json_results = []
# #print(results)
# df = pd.DataFrame(results)
# for name, group in df.groupby('topic'):
#     mean_value = group['value'].mean()
#     json_value = {"topic":name,"field":record.get_field(),"value":mean_value}
#     json_results.append(json_value)
        
# a =  {"data":json_results}      
# print(type(a))
# print(a["data"][0]["topic"])
Influx = InfluxDataBase(URL,TOKEN,ORG)
@app.get("/read/latest")
async def fetch_movies():
    try:
        return Influx.read_data_latest()
    except:
        raise HTTPException(status_code=404, detail="Something has problem")
    
@app.get("/")
async def fetch_movies():
    try:
        return "sfdsdfsdf"
    except:
        raise HTTPException(status_code=404, detail="Something has problem")

@app.get("/test")
async def test():
    return "complete system"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)