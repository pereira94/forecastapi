import urllib3
import json
import pandas as pd
import datetime
import boto3
import os
from os import listdir
from os.path import isfile, join

s3_client = boto3.client("s3")
LOCAL_FILE_SYS = "/tmp"
S3_BUCKET = os.environ['s3bucket']

def get_key():
    from datetime import datetime
    dt_now = datetime.now()
    key = (
        dt_now.strftime("%Y-%m-%d")
        + "-"
         + dt_now.strftime("%H")
        + "-"
        + dt_now.strftime("%M")
    )
    return key

def unix_datetime(unix_time):
    x = datetime.datetime.fromtimestamp(
        (int(unix_time)/1000)
    ).strftime('%Y-%m-%d %H:%M:%S')
    return x

def get_data():
    http = urllib3.PoolManager()
    r = http.request(
            "GET",
            'https://api.coincap.io/v2/rates/ethereum')
    data = json.loads(r.data.decode("utf8").replace("'", '"'))
    x = pd.json_normalize(data)
    x = x[['timestamp', 'data.rateUsd']]
    x['datetime'] = unix_datetime(x['timestamp'])
    x.rename(columns={'data.rateUsd':'priceUsd'})
    return x

key = get_key()

def write_to_local():
    data = get_data()
    filename = LOCAL_FILE_SYS + "/" + str(key) + ".csv"
    data.to_csv(filename)


def lambda_handler(event,context):
    write_to_local()
    files = [f for f in listdir(LOCAL_FILE_SYS) if isfile(join(LOCAL_FILE_SYS, f))]
    for f in files:
        s3_client.upload_file(LOCAL_FILE_SYS + "/" + f, S3_BUCKET, f)





