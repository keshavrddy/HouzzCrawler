from bs4 import BeautifulSoup
import uuid
import json
import os
import boto3
from boto3.s3.transfer import S3Transfer
import requests
import wget
import ssl
from functools import wraps
from config import ConfigSectionMap
from houzzCrawler import Data

cfg = ConfigSectionMap('aws')

def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar
ssl.wrap_socket = sslwrap(ssl.wrap_socket)

client = boto3.client(
    's3',
    aws_access_key_id=cfg['aws_access_key_id'],
    aws_secret_access_key=cfg['aws_secret_access_key']
)

transfer = S3Transfer(client)
ssl._create_default_https_context = ssl._create_unverified_context
w = open("/Users/keshavreddy/PersonalProjects/Data/HM_Urls/61.txt", "r")
urls = []
w = w.readlines()

for COUNT,url in enumerate(urls[8052:], start=8052):
    if '/pro/' in url:
        unique_id = uuid.uuid4().hex
        print(COUNT, url)
        user_data = Data(url)
        file = open('/Users/keshavreddy/PersonalProjects/Data/json/' + str(unique_id) + '.json', 'wt')
        file.write(json.dumps(user_data,ensure_ascii=False))
        file.close()
        transfer.upload_file('/Users/keshavreddy/PersonalProjects/Data/json/' +
                             str(unique_id) + '.json', 'housemundynew',
                             'Json_dump1/{}.json'.format(str(unique_id)))
        os.remove('/Users/keshavreddy/PersonalProjects/Data/json/{}.json'.format(str(unique_id)))





