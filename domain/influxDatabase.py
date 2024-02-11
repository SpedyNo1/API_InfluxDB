from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
pd.set_option('display.max_columns', None)

class InfluxDataBase:
    def __init__(self,url,token,org) -> None:
        self.client=InfluxDBClient(url=url,token=token,org=org)
        self.write_api=self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api=self.client.query_api()
        self.token=token
        self.org=org
        
    def read_data_latest(self):
        query = f'from(bucket: "Devices")'  
        query += f'|> range(start: -5m)'
        query += f'|> filter(fn:(r) => r["_measurement"] == "mqtt_consumer")'
        # query += f'|> filter(fn: (r) => r._field == "DO_value" or r._field == "temp")'
        # query=query+f'|> filter(fn: (r) => r["topic"] == "sgm/factory/1703407002")'
        result = self.query_api.query(org=self.org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append({"time":record.get_time(),"field":record.get_field(),"value":record.get_value(),"topic":record.values.get("topic")})
        json_results = []
        if not results:
            return {"data":[]}
        df = pd.DataFrame(results)
        df = df[df['topic'].str.startswith('devices/iot/')].sort_values(by='time')
        count_unique = df['field'].unique()   
        for field in count_unique:
            buffer = df[(df["field"] == field)] 
            for name, group in buffer.groupby('topic'):
                mean_value = group['value'].mean()
                json_value = {"topic":name,group['field'].unique()[0]:mean_value}
                json_results.append(json_value)  
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
        return {"data":result_list}
