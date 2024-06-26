import requests
import json
import os
import datetime

appID = os.environ.get("APP_ID")
appSecret = os.environ.get("APP_SECRET")
openId = os.environ.get("OPEN_ID")

def get_weather():
    url="https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=tc"
    resp = requests.get(url)
    data=resp.json()
    generalSituation=data["generalSituation"]
    tcInfo="無" if data["tcInfo"]=="" else data["tcInfo"]
    forecastPeriod=data["forecastPeriod"]
    forecastDesc=data["forecastDesc"]
    outlook=data["outlook"]
    updateTime=data["updateTime"]
    return generalSituation, tcInfo, forecastPeriod,forecastDesc,updateTime

def get_tomorrow_weather():
    url="https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc"
    resp = requests.get(url)
    data=resp.json()
    general=data["generalSituation"]
    weather=data["weatherForecast"][0]["forecastWeather"]
    wind=data["weatherForecast"][0]["forecastWind"]
    tempMax=data["weatherForecast"][0]["forecastMaxtemp"]["value"]
    tempMin=data["weatherForecast"][0]["forecastMintemp"]["value"]
    humMax=data["weatherForecast"][0]["forecastMaxrh"]["value"]
    humMin=data["weatherForecast"][0]["forecastMinrh"]["value"]
    return general,weather,wind,tempMax,tempMin,humMax,humMin

def get_weather_warn():
    url="https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warningInfo&lang=tc"
    resp = requests.get(url)
    data=resp.json()
    if data !={}:
        data=resp.json()["details"]
        len_data=len(data)
        warn=""
        for i in range(0,len_data):
            warn+=str(data[i]["contents"])+"\r\n"
    else:
        warn="無\r\n"
    # print(warn)
    return warn

def get_rainfall():
    url="https://data.weather.gov.hk/weatherAPI/opendata/hourlyRainfall.php?lang=tc"
    resp = requests.get(url)
    data=resp.json()["hourlyRainfall"]
    len_data=len(data)
    for i in range(0,len_data):
        if data[i]["automaticWeatherStation"]=="香港天文台":
            rain=data[i]["value"]+" "+data[i]["unit"]
    return rain

def get_earthquake():
    url="https://data.weather.gov.hk/weatherAPI/opendata/earthquake.php?dataType=qem&lang=tc"
    resp = requests.get(url)
    data=resp.json()
    if data !={}:
        ptime = datetime.datetime.strptime(data["ptime"], "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S")
        updatetime = datetime.datetime.strptime(data["updateTime"], "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S")
        earthquake=data["region"]+"(緯度"+str(data["lat"])+", 經度"+str(data["lon"])+")"+"\r\n芮氏地震規模: "+str(data["mag"])+"\r\n地震時間: "+str(ptime)+"\r\n更新時間: "+str(updatetime)
    else:
        earthquake="無\r\n"
    return earthquake

def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    # print(response)
    access_token = response.get('access_token')
    return access_token

def send_weather_text(access_token, weather,tomo_weather,warn,rain,earthquake):
    import datetime
    today = datetime.date.today()
    today_str = today.strftime("%Y年%m月%d日")

    body = {
        "touser": openId.strip(),
        "text":{           
            "content":"本港地區天氣預報(HKO "+weather[4][11:16]+"更新)\r\n"+"\r\n過去一小時雨量: "+rain+"\r\n"+weather[2]+"：\r\n"+weather[3]+"\r\n\r\n明日天氣：\r\n"+tomo_weather[1]+tomo_weather[2]+"溫度"+str(tomo_weather[4])+"°C ~ "+str(tomo_weather[3])+"°C。"+"相對濕度"+str(tomo_weather[6])+"% ~ "+str(tomo_weather[5])+"%。"+"\r\n\r\n特別天氣提示：\r\n"+warn+"\r\n地震速報: \r\n"+earthquake+"\r\n\r\n熱帶氣旋：\r\n"+weather[1]
        },     
        "msgtype":"text"
        }
    url = 'https://api.weixin.qq.com/cgi-bin/message/mass/preview?access_token={}'.format(access_token)
    print(requests.post(url, data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')))


def weather_report():
    access_token = get_access_token()
    weather = get_weather()
    tomo_weather=get_tomorrow_weather()
    warn=get_weather_warn()
    rain=get_rainfall()
    earthquake=get_earthquake()
    print(f"天气信息： {weather,tomo_weather,warn,rain,earthquake}")
    send_weather_text(access_token, weather,tomo_weather,warn,rain,earthquake)

if __name__ == '__main__':
    weather_report()
