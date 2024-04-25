import requests
import json
import os


# 从测试号信息获取
appID = os.environ.get("APP_ID")
appSecret = os.environ.get("APP_SECRET")
# 收信人ID即 用户列表中的微信号
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
    # hum=data["forecastMaxrh"]
    general=data["generalSituation"]
    weather=data["weatherForecast"][0]["forecastWeather"]
    wind=data["weatherForecast"][0]["forecastWind"]
    tempMax=data["weatherForecast"][0]["forecastMaxtemp"]["value"]
    tempMin=data["weatherForecast"][0]["forecastMintemp"]["value"]
    humMax=data["weatherForecast"][0]["forecastMaxrh"]["value"]
    humMin=data["weatherForecast"][0]["forecastMinrh"]["value"]
    return general,weather,wind,tempMax,tempMin,humMax,humMin


def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    # print(response)
    access_token = response.get('access_token')
    return access_token

def send_weather_text(access_token, weather,tomo_weather):
    import datetime
    today = datetime.date.today()
    today_str = today.strftime("%Y年%m月%d日")

    body = {
        "touser": openId.strip(),
        "text":{           
            "content":"本港地區天氣預報(數據源自：香港天文臺)\r\n"+"天氣概況："+weather[0]+"\r\n"+weather[2]+"："+weather[3]+"\r\n明日天氣："+tomo_weather[1]+tomo_weather[2]+"溫度"+str(tomo_weather[4])+"°C ~ "+str(tomo_weather[3])+"°C。"+"相對濕度"+str(tomo_weather[6])+"% ~ "+str(tomo_weather[5])+"%。"+"\r\n未來天氣："+tomo_weather[0]+"\r\n熱帶氣旋："+weather[1]+"\r\n更新時間："+weather[4]
        },     
        "msgtype":"text"
        }
    url = 'https://api.weixin.qq.com/cgi-bin/message/mass/preview?access_token={}'.format(access_token)
    print(requests.post(url, data=bytes(json.dumps(body, ensure_ascii=False), encoding='utf-8')))


def weather_report():
    # 1.获取access_token
    access_token = get_access_token()
    # 2. 获取天气
    weather = get_weather()
    tomo_weather=get_tomorrow_weather()
    print(f"天气信息： {weather,tomo_weather}")
    # 3. 发送消息
    send_weather_text(access_token, weather,tomo_weather)


if __name__ == '__main__':
    weather_report()
