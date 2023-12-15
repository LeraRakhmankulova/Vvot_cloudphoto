import configparser
from pathlib import Path
import sys

from init import create_s3_session, get_config_file_path, get_init_info

def is_album_exist(session, bucket, album):
    list_objects = session.list_objects(
        Bucket=bucket,
        Prefix=album + '/',
        Delimiter='/',
    )
    if "Contents" in list_objects:
        for _ in list_objects["Contents"]:
            return True
    return False


def download_photos(album, path):
    path = Path(path)

    get_init_info()

    config_file = get_config_file_path()
    config = configparser.ConfigParser()
    config.read(config_file)
    bucket = config['DEFAULT'].get('bucket')

    s3 = create_s3_session(config['DEFAULT'].get(
        'aws_access_key_id'), config['DEFAULT'].get('aws_secret_access_key'))

    if not is_album_exist(s3, bucket, album):
        print("Album does not exist")
        sys.exit(1)
    
    if not path.is_dir():
        print(f"{str(path)} is not directory")
        sys.exit(1)


    list_object = s3.list_objects(Bucket=bucket, Prefix=album + '/', Delimiter='/')
    for key in list_object["Contents"]:
        obj = s3.get_object(Bucket=bucket, Key=key["Key"])
        if obj['ContentType'] != 'image/jpeg':
            continue

        filename = Path(key['Key']).name
        filepath = path / filename
        with filepath.open("wb") as file:
            file.write(obj["Body"].read())
    print("Album downloaded successfully")
    sys.exit(0)