import os
import configparser
import sys
import boto3
from botocore.exceptions import ClientError


def get_init_info():
    config_file = get_config_file_path()

    if not os.path.isfile(config_file):
        print("Configuration file not exist. Use 'init' command.")
        return

    config = configparser.ConfigParser()
    config.read(config_file)

    required_params = ['bucket', 'aws_access_key_id', 'aws_secret_access_key', 'region', 'endpoint_url']

    for param in required_params:
        if not config['DEFAULT'].get(param):
            print(f"Missing {param} in the configuration file. Use 'init' command to initialize.")
            sys.exit(1)
        

def create_s3_session(access_key, secret_access_key):
    session = boto3.session.Session()
    return session.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        region_name='ru-central1',
    )


# Функция для получения пути к файлу конфигурации
def get_config_file_path():
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".config", "cloudphoto")
    os.makedirs(config_dir, exist_ok=True)
    config_file = os.path.join(config_dir, "cloudphotorc")
    return config_file


# Функция для инициализации приложения
def initialize():
    config_file = get_config_file_path()
    config = configparser.ConfigParser()
    config.read(config_file)
        
    aws_access_key_id = input("AWS Access Key ID: ")
    aws_secret_access_key = input("AWS Secret Access Key: ")
    bucket = input("Bucket: ")

    config['DEFAULT'] = {
        'bucket': bucket,
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key,
        'region': 'ru-central1',
        'endpoint_url': 'https://storage.yandexcloud.net'
    }

    with open(config_file, 'w') as configfile:
        config.write(configfile)

    try:
        s3 = create_s3_session(aws_access_key_id, aws_secret_access_key )
        s3.create_bucket(Bucket=bucket, ACL='public-read-write')
    except ClientError as clientError:
        if clientError.response["Error"]["Code"] != "BucketAlreadyOwnedByYou":
            print(clientError)
            sys.exit(1)
