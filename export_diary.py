#!/usr/bin/env python3

import json
import os
import shutil
from base64 import b64encode

import yaml

from export_diary import *

import numpy as np
import pandas as pd

import requests
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
load_dotenv()

def main():
    #xls = read_diary()
    xls = export_diary()
    save_diary(xls)
    get_favorite_food(xls)

def export_diary():

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

    print('===DOWNLOAD==')
    print (download)

    return download.content

def get_favorite_food(download):

    xls = pd.ExcelFile(download)

    df = pd.read_excel(xls, index_col=None)
    d = df.to_dict(orient='index')

    mostrecentfood ="- " + d[len(d)-1]['Amount']+' '+d[len(d)-1]['Name']

    with open('recent_food.yml', 'w') as file:
        file.write(mostrecentfood)

def save_diary(download):
    with open('NewDiary.xls', 'wb') as file:
        file.write(download)

def read_diary():
    with open('NewDiary.xls', 'rb') as file:
        return file.read()

if __name__ == "__main__":
    main()
