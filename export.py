#!/usr/bin/env python3

import json
import os
import shutil
from base64 import b64encode

import yaml

import numpy as np
import pandas as pd

import requests
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
load_dotenv()

login = os.environ['MY_NET_DIARY_LOGIN']
password = os.environ['MY_NET_DIARY_PASSWORD']


auth_url = 'https://www.mynetdiary.com/muiSignIn.do'
data_url = 'https://www.mynetdiary.com/exportData.do?year=2021'

headers = {
    'Content-Type': 'application/json',
}

payload_dict = {"login":login,"password":password,"rememberMe":"true"}

data = json.dumps(payload_dict)


s = requests.Session()
auth = s.post('http://www.mynetdiary.com/muiSignIn.do', headers=headers, data=data, auth=('login', 'password'))

print('===AUTH===')
print (auth)

download = s.get(data_url)

print('===DOWNLOAD===')
print (download)

with open('NewDiary.xls', 'wb') as file:
    file.write(download.content)
