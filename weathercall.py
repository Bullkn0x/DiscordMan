from datetime import datetime, timedelta
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
    #print(json_data)
    dt_object = datetime.fromtimestamp(json_data['currently']['time'])
    print("TIME IS: ", dt_object)


    # adding and subtracting time using +-timedelta(days, minutes, seconds)
    for each in json_data['daily']['data']:
        print("Date: ", (datetime.fromtimestamp(each['time'])).strftime('%m/%d/%Y'))
        print("Summary ", each['summary'])
        print("High ", each['temperatureHigh'])
        print("Low ", each['temperatureLow'])

    #print("time is " , datetime.fromtimestamp(json_data['daily']['data'][0]['time']))
    #print("time is " , datetime.fromtimestamp(json_data['daily']['data'][1]['time']))
    #print("time is " , datetime.fromtimestamp(json_data['daily']['data'][2]['time']))
    #print("time is " , datetime.fromtimestamp(json_data['daily']['data'][3]['time']))
    #print("type(dt_object) =", type(dt_object))

if __name__ == '__main__':
    weatherdata()