import os
import requests

cookie = os.environ.get("JD_COOKIE")
url = os.environ.get("JD_URL")

headers = {"Connection": 'keep-alive',
           "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
           "Cache-Control": 'no-cache',
           "User-Agent": "okhttp/3.12.1;jdmall;android;version/10.3.4;build/92451;",
           "accept": "*/*",
           "connection": "Keep-Alive",
           "Accept-Encoding": "gzip, deflate, br",
           "Cookie": cookie
           }

response = requests.post(url=url, headers=headers)
print(response.text)
