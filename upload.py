import configparser
import sys
from init import create_s3_session, get_config_file_path, get_init_info
from pathlib import Path

def is_image(file):
    return file.is_file() and file.suffix in [".jpg", ".jpeg"]


def upload_photos(album, path):
    path = Path(path)
    # проверка конфигурационного файла
    get_init_info()

    config_file = get_config_file_path()
    config = configparser.ConfigParser()
    config.read(config_file)
    bucket = config['DEFAULT'].get('bucket')

    if not bucket:
        print("Bucket name is not defined.")
        sys.exit(1)
    s3 = create_s3_session(config['DEFAULT'].get(
        'aws_access_key_id'), config['DEFAULT'].get('aws_secret_access_key'))


    if not path.is_dir():
        print(f'{path} folder does not exist')
        sys.exit(1)

    # Проверяем наличие фотоальбома
    response = s3.list_objects(Bucket=bucket, Prefix=f"{album}/")
    album_exists = 'Contents' in response

    # Создаем фотоальбом, если он не существует
    if not album_exists:
        s3.put_object(Body='', Bucket=bucket, Key=f"{album}/")


    count = 0
    for file in path.iterdir():
        if is_image(file):
            try:
                key = f"{album}/{file.name}"
                s3.upload_file(str(file), bucket, key)
                count += 1
            except Exception as ex:
                print(f'Error: {ex}')
                sys.exit(1)

    if not count:
        print(f"There are no images with image extensions in the specified folder")
        sys.exit(1)
    
    print("Upload completed successfully.")
    sys.exit(0)
