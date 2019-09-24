from datetime import datetime
import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()
DARK_TOKEN=os.getenv('DARK_SKY_API')

def weatherdata():
    url = f'https://api.darksky.net/forecast/{DARK_TOKEN}/42.3601,-71.0589'
    response = requests.get(url)
    print("response is ",response)
    data = response.text
    json_data = json.loads(data)
    print(json_data)
    dt_object = datetime.fromtimestamp(json_data['currently']['time'])
    print("TIME IS: ", dt_object)
    #print("type(dt_object) =", type(dt_object))

if __name__ == '__main__':
    weatherdata()