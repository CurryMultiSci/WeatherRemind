import requests
import json
import os


# 从测试号信息获取
appID = os.environ.get("APP_ID")
appSecret = os.environ.get("APP_SECRET")
# 收信人ID即 用户列表中的微信号
openId = os.environ.get("OPEN_ID")
# 天气预报模板ID
weather_template_id = os.environ.get("TEMPLATE_ID")


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
    print(response)
    access_token = response.get('access_token')
    return access_token

def send_weather(access_token, weather,tomo_weather):
    # touser 就是 openID
    # template_id 就是模板ID
    # url 就是点击模板跳转的url
    # data就按这种格式写，time和text就是之前{{time.DATA}}中的那个time，value就是你要替换DATA的值

    import datetime
    today = datetime.date.today()
    today_str = today.strftime("%Y年%m月%d日")

    body = {
        "touser": openId.strip(),
        "template_id": weather_template_id.strip(),
        "url": "https://weixin.qq.com",
        "data": {
            "date": {
                "value": today_str
            },
            "generalSituation": {
                "value": weather[0]
            },
            "forecastPeriod": {
                "value": weather[2]
            },
            "forecastDesc": {
                "value": weather[3]
            },
            "tcInfo": {
                "value": weather[1]
            },
            "updateTime": {
                "value": weather[4]
            },
            "tomo_general": {
                "value": tomo_weather[0]
            },
            "tomo_weather": {
                "value": tomo_weather[1]
            },
            "tomo_wind": {
                "value": tomo_weather[2]
            },
            "tomo_tempmax": {
                "value": tomo_weather[3]
            },
            "tomo_tempmin": {
                "value": tomo_weather[4]
            },
            "tomo_hummax": {
                "value": tomo_weather[5]
            },
            "tomo_hummin": {
                "value": tomo_weather[6]
            }
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    print(requests.post(url, json.dumps(body)).text)


def weather_report():
    # 1.获取access_token
    access_token = get_access_token()
    # 2. 获取天气
    weather = get_weather()
    tomo_weather=get_tomorrow_weather()
    print(f"天气信息： {weather,tomo_weather}")
    # 3. 发送消息
    send_weather(access_token, weather,tomo_weather)


if __name__ == '__main__':
    weather_report()
