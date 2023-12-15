import configparser
from os import path
import os
import random
from pathlib import Path
import pathlib
import shutil
import string
import sys
from init import create_s3_session, get_config_file_path, get_init_info
from jinja2 import Template

ROOT_DIRECTORY = path.dirname(pathlib.Path(__file__))
SITE_CONFIGURATION = {
    "ErrorDocument": {"Key": "error.html"},
    "IndexDocument": {"Suffix": "index.html"},
}

def get_template(name):
    template_path = Path(ROOT_DIRECTORY) / "templates" / name
    with open(template_path, "r") as file:
        return file.read()


def save_temporary_template(template) -> str:
    filename = ''.join(random.choices(
        string.ascii_letters + string.digits, k=8)) + ".html"
    path = Path(ROOT_DIRECTORY) / "temp" / filename
    if not path.parent.exists():
        os.mkdir(path.parent)

    with open(path, "w") as file:
        file.write(template)

    return str(path)

def remove_temporary_dir():
    path = Path(ROOT_DIRECTORY) / "temp"
    shutil.rmtree(path)

    
def mksite():
    get_init_info()

    config_file = get_config_file_path()
    config = configparser.ConfigParser()
    config.read(config_file)
    bucket = config['DEFAULT'].get('bucket')

    url = f"https://{bucket}.website.yandexcloud.net"
    template = get_template("album.html")

    s3 = create_s3_session(config['DEFAULT'].get(
        'aws_access_key_id'), config['DEFAULT'].get('aws_secret_access_key'))

    s3.put_bucket_acl(ACL='public-read', Bucket=bucket)

    albums = {}
    list_objects = s3.list_objects(Bucket=bucket)
    for key in list_objects["Contents"]:
        album_img = key["Key"].split("/")
        if len(album_img) != 2:
            continue
        album, img = album_img
        if album in albums:
            albums[album].append(img)
        else:
            albums[album] = [img]

    albums_rendered = []
    i = 1
    for album, photos in albums.items():
        template_name = f"album{i}.html"
        rendered_album = Template(template).render(
            album=album, images=photos, url=url)
        path = save_temporary_template(rendered_album)

        s3.upload_file(path, bucket, template_name)
        albums_rendered.append({"name": template_name, "album": album})
        i += 1

    template = get_template("index.html")
    rendered_index = Template(template).render(
        template_objects=albums_rendered)
    path = save_temporary_template(rendered_index)
    s3.upload_file(path, bucket, "index.html")

    template = get_template("error.html")
    path = save_temporary_template(template)
    s3.upload_file(path, bucket, "error.html")

    s3.put_bucket_website(
        Bucket=bucket, WebsiteConfiguration=SITE_CONFIGURATION)
    remove_temporary_dir()
    
    print(url)
    sys.exit(0)

