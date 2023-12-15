import configparser
import sys
from init import create_s3_session, get_config_file_path, get_init_info

def delete_photos(album, photo):
    get_init_info()

    config_file = get_config_file_path()
    config = configparser.ConfigParser()
    config.read(config_file)

    s3 = create_s3_session(config['DEFAULT'].get(
        'aws_access_key_id'), config['DEFAULT'].get('aws_secret_access_key'))

    bucket = config['DEFAULT'].get('bucket')

    if photo is not None:
        photo_key = album + '/' + photo

        s3.delete_objects(
            Bucket=bucket, Delete={"Objects": [{"Key": photo_key}]}
        )
        print('Image deleted successfully')
        sys.exit(0)

    # удалить в облачном хранилище все фотографии из альбома
    list_objects = s3.list_objects(
        Bucket=bucket,
        Prefix=album + '/',
        Delimiter='/',
    )["Contents"]
    img_keys = [{"Key": img_key.get('Key')} for img_key in list_objects]

    s3.delete_objects(Bucket=bucket, Delete={"Objects": img_keys})
    print('Images and album deleted successfully')
    sys.exit(0)
    

    