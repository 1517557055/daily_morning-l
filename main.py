from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_idd = os.environ["USER_IDD"]
template_id = os.environ["TEMPLATE_ID"]

app_key = os.environ["APP_KEY"]
constellation = os.environ["CONSTELLATION"]

sisname = os.environ["USER_NAME"]

def get_constellation():
  
  url = "http://web.juhe.cn/constellation/getAll?"
  params = {
    "key": app_key,
    "consName": constellation,
    "type": "today"
  }
  response = requests.get(url, params=params).json()
  
  if response["resultcode"] == "200":
    retnum = response["number"]
    retcolor = response["color"]
    retdate = response["datetime"]
  return retnum,retcolor,retdate

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
luckynum, luckycolor, todate = get_constellation()
wea, temperature = get_weather()
data = {"lucknum":{"value":luckynum, "color":get_random_color()},"luckcolor":{"value":luckycolor, "color":get_random_color()},"date":{"value":todate, "color":get_random_color()},"city":{"value":city, "color":get_random_color()},"weather":{"value":wea, "color":get_random_color()},"temperature":{"value":temperature, "color":get_random_color()},"love_days":{"value":get_count(), "color":get_random_color()},"sis_name":{"value":sisname, "color":get_random_color()},"birthday_left":{"value":get_birthday(), "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}

res = wm.send_template(user_idd, template_id, data)
print(res)
