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
pig_city = os.environ['PIG_CITY']
birthday = os.environ['BIRTHDAY']
pig_birthday = os.environ['PIG_BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  low=math.floor(weather['low'])
  high=math.floor(weather['high'])
  air=weather['airQuality']
  wind=weather['wind']
  return weather['weather'], math.floor(weather['temp']),low,high,wind,air

def get_pig_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + pig_city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  low = math.floor(weather['low'])
  high = math.floor(weather['high'])
  air = weather['airQuality']
  wind = weather['wind']
  return weather['weather'], math.floor(weather['temp']),low,high,wind,air

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_pig_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + pig_birthday, "%Y-%m-%d")
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
wea, temperature,low, high,wind,air= get_weather()
pig_wea, pig_temperature,pig_low, pig_high,pig_wind,pig_air = get_pig_weather()
data = {"weather":{"value":wea, "color":get_random_color()},"temperature":{"value":temperature, "color":get_random_color()},"low":{"value":low, "color":get_random_color()},"high":{"value":high, "color":get_random_color()},"wind":{"value":wind, "color":get_random_color()},"air":{"value":air, "color":get_random_color()},"pig_weather":{"value":pig_wea, "color":get_random_color()},"pig_temperature":{"value":pig_temperature, "color":get_random_color()},"pig_low":{"value":pig_low, "color":get_random_color()},"pig_high":{"value":pig_high, "color":get_random_color()},"pig_wind":{"value":pig_wind, "color":get_random_color()},"pig_air":{"value":pig_air, "color":get_random_color()},"love_days":{"value":get_count(), "color":get_random_color()},"birthday_left":{"value":get_birthday(), "color":get_random_color()},"birthday_right":{"value":get_pig_birthday(), "color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
