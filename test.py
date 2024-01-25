import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
pd.set_option('display.max_columns', None)
from config import (
    URL,TOKEN,ORG,BROKER,PORT,TOPIC,CLIENT_ID,MQTT_USERNAME,MQTT_PASSWORD,TELEGRAF
)
bucket = "<my-bucket>"
org = "hadyai-iot"
token = "UeeDmS1TFY-oWgV9I_xH6nsR-Yeo7K1rZeX5zSVc3bwmi2_y9Tz403v7yLFNh3CFOLOTXa8GQ_MuNAhUJLJ2Vw=="
# Store the URL of your InfluxDB instance
url="https://us-east-1-1.aws.cloud2.influxdata.com"
client = influxdb_client.InfluxDBClient(
    url=URL,
    token=TOKEN,
    org=ORG
)
query_api = client.query_api()
class Test:
    def __init__(self,bucket, field, measureament_name):
        self.bucket = bucket
        self.field = field
        self.measureament_name = measureament_name

# data = Test("sensor",["DO_value","temp"],"mqtt_consumer")
# json_results = []
# for field in data.field:
#     query = f'from(bucket: "{data.bucket}")'  
#     query += f'|> range(start: -30m, stop: now())'
#     query += f'|> filter(fn:(r) => r["_measurement"] == "{data.measureament_name}")'
#     query += f'|> filter(fn:(r) => r["_field"] == "{field}")'
#     result = query_api.query(org=org, query=query)
#     results = []
#     for table in result:
#         for record in table.records:
#             results.append({"time":record.get_time(),"field":record.get_field(),"value":record.get_value(),"topic":record.values.get("topic")})
#     #print(results)
#     df = pd.DataFrame(results)
#     df = df[df['topic'].str.startswith('sgm/factory/')].sort_values(by='time')
#     #print(df)

#     for name, group in df.groupby('topic'):
#         mean_value = group['value'].mean()
#         json_value = {"topic":name,"field":record.get_field(),"value":mean_value}
#         json_results.append(json_value)
        
# a={"data":json_results} 
# print(a)
#------------------------------------------------------------------------------------
# query = f'from(bucket: "sensor")'  
# query += f'|> range(start: -60m)'
# query += f'|> filter(fn:(r) => r["_measurement"] == "mqtt_consumer")'
# # query += f'|> filter(fn: (r) => r._field == "DO_value" or r._field == "temp")'
# # query=query+f'|> filter(fn: (r) => r["topic"] == "sgm/factory/1703407002")'

# result = query_api.query(org=ORG, query=query)
# results = []
# for table in result:
#     for record in table.records:
#         results.append({"time":record.get_time(),"field":record.get_field(),"value":record.get_value(),"topic":record.values.get("topic")})
# json_results = []
# #print(results)
# df = pd.DataFrame(results)
# df = df[df['topic'].str.startswith('sgm/factory/')].sort_values(by='time')
# #print(df)  
# count_unique = df['field'].unique()   
# #count_unique = ['conductivity_value' ,'DO_value' ,'pH_value']# Apply unique function
# print(count_unique)
# for field in count_unique:
#     #print(field)
#     buffer = df[(df["field"] == field)] 
#     print(buffer)
#     for name, group in buffer.groupby('topic'):
#         #print(name)
#         #print(group)
#         mean_value = group['value'].mean()
#         json_value = {"topic":name,group['field'].unique()[0]:mean_value}
#         json_results.append(json_value)  
#         #print("-----------------------")
#     #print("++++++++++++++++++")
# print(json_results)
# data = json_results
# merged_data = {}

# for item in data:
#     topic = item['topic']
#     if topic not in merged_data:
#         merged_data[topic] = {}
#     for key, value in item.items():
#         if key != 'topic':
#             merged_data[topic][key] = value

# result_list = [{'topic': topic, **values} for topic, values in merged_data.items()]
# print({"data":result_list})
                      
class Test:
    def __init__(self,url,token,org) -> None:
        self.client=influxdb_client.InfluxDBClient(url=url,token=token,org=org)
        self.write_api=self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api=self.client.query_api()
        self.url=url
        self.token=token
        self.org=org
    def read(self):
        query = f'from(bucket: "sensor")'  
        query += f'|> range(start: -5m)'
        query += f'|> filter(fn:(r) => r["_measurement"] == "mqtt_consumer")'
        #query += f'|> filter(fn: (r) => r._field == "DO_value" or r._field == "temp")'
        #query += f'|> filter(fn: (r) => r["topic"] == "sgm/factory/1703407002")'
        result = self.query_api.query(org=self.org, query=query)
        #print(result)
        results = []
        for table in result:
            for record in table.records:
                results.append({"time":record.get_time(),"field":record.get_field(),"value":record.get_value(),"topic":record.values.get("topic")})
        json_results = []
        #print(results)
        df = pd.DataFrame(results)
        print(df) 
        df = df[df['topic'].str.startswith('sgm/factory/')].sort_values(by='time')
        #print(df)  
        count_unique = df['field'].unique()   
        #count_unique = ['conductivity_value' ,'DO_value' ,'pH_value']# Apply unique function
        #print(count_unique)
        for field in count_unique:
            #print(field)
            buffer = df[(df["field"] == field)] 
            #print(buffer)
            for name, group in buffer.groupby('topic'):
                #print(name)
                #print(group)
                mean_value = group['value'].mean()
                json_value = {"topic":name,group['field'].unique()[0]:mean_value}
                json_results.append(json_value)  
                #print("-----------------------")
            #print("++++++++++++++++++")
        #print(json_results)
        data = json_results
        merged_data = {}

        for item in data:
            topic = item['topic']
            if topic not in merged_data:
                merged_data[topic] = {}
            for key, value in item.items():
                if key != 'topic':
                    merged_data[topic][key] = value

        result_list = [{'topic': topic, **values} for topic, values in merged_data.items()]
        # print({"data":result_list})
        return {"data":result_list}
    
influx = Test(URL,TOKEN,ORG)
print(influx.read())

