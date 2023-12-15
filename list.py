import configparser
from pathlib import Path
import sys
from init import create_s3_session, get_config_file_path, get_init_info


def list_photos(album):
    get_init_info()

    config_file = get_config_file_path()
    config = configparser.ConfigParser()
    config.read(config_file)
    bucket = config['DEFAULT'].get('bucket')

    s3 = create_s3_session(config['DEFAULT'].get(
        'aws_access_key_id'), config['DEFAULT'].get('aws_secret_access_key'))
    
    list_objects = s3.list_objects(
        Bucket=bucket,
        Prefix=album + '/',
        Delimiter='/'
    )

    images = []
    for key in list_objects["Contents"]:
        images.append(Path(key["Key"]).name)

    if not len(images):
        print("No images")
        sys.exit(1)

    for photo_name in images:
        if not (photo_name.endswith('.jpg') or photo_name.endswith('.jpeg')): 
            continue
        print(f"# {photo_name}")
    sys.exit(0)


def list_albums():
    get_init_info()

    config_file = get_config_file_path()
    config = configparser.ConfigParser()
    config.read(config_file)
    bucket = config['DEFAULT'].get('bucket')
    
    s3 = create_s3_session(config['DEFAULT'].get(
        'aws_access_key_id'), config['DEFAULT'].get('aws_secret_access_key'))
    
    list_objects = s3.list_objects(Bucket=bucket)

    albums = set()
    if "Contents" in list_objects:
        for key in list_objects["Contents"]:
            res = (key['Key']).split("/", 1)[0]
            if res.endswith('.jpg') or res.endswith('.jpeg') : continue
            albums.add(res)

    if not len(albums):
        print(f"Is no albums in {bucket}")
        sys.exit(1)

    for album in albums:
        print(f"# {album}")
    sys.exit(0)