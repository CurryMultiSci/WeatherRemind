import os
import requests

cookie = os.environ.get("JD_COOKIE")
fID=os.environ.get("JD_fID")
url = ("https://api.m.jd.com/client.action")

headers = {"Connection": 'keep-alive',
           "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
           "Cache-Control": 'no-cache',
           "User-Agent": "jdapp;iPhone;12.4.3;;;M/5.0;appBuild/169159;",
           "accept": "*/*",
           "connection": "Keep-Alive",
           "Accept-Encoding": "gzip, deflate, br",
           "Cookie": cookie,
           "functionId":fID
           }

response = requests.post(url=url, headers=headers)
print(response.text)
