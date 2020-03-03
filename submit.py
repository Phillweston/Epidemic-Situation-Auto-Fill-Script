#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import requests
import re
import sys
import datetime
import time

h=1
m=0

with open("data.json", "r") as fd:
    data = json.load(fd)

conn = requests.Session()

# Login
result = conn.post('https://xxcapp.xidian.edu.cn/uc/wap/login/check',
               data={'username': data['_u'], 'password': data['_p']})
if result.status_code != 200:
    print('认证大失败')
    exit()

# Submit
result = conn.get('https://xxcapp.xidian.edu.cn/ncov/wap/default/index')
if result.status_code != 200:
    print('获取页面大失败')
    exit()
predef = json.loads(re.search('var def = ({.*});', result.text).group(1))

if "dump_geo" in sys.argv:
    print(predef['geo_api_info'])
    exit()

try:
    del predef['jrdqtlqk']
    del predef['jrdqjcqk']
except:
    pass
del data['_u']
del data['_p']
predef.update(data)

while True:
    now = datetime.datetime.now()
    print(now.hour, now.minute)
    if now.hour == h and now.minute == m:
        result = conn.post('https://xxcapp.xidian.edu.cn/ncov/wap/default/save', data=predef)
        print(result.text)
    # 每隔60秒检测一次
    time.sleep(60)
