from argparse import ArgumentParser

from init import initialize
from upload import upload_photos
from download import download_photos
from list import list_albums, list_photos
from delete import delete_photos
from mksite import mksite

def main():
    # Считывание команды и опций 
    parser = ArgumentParser(description='CloudPhoto CLI')
    subparsers = parser.add_subparsers(title='Commands', dest='command',)

    # Команда upload
    upload_parser = subparsers.add_parser('upload', help='Upload photos')
    upload_parser.add_argument('--album', required=True, help='Name of the album')
    upload_parser.add_argument('--path', default='.', help='Photos directory')

    # Команда download
    download_parser = subparsers.add_parser('download', help='Download photos')
    download_parser.add_argument('--album', required=True, help='Name of the album')
    download_parser.add_argument('--path', default='.', help='Photos directory')

    # Команда list
    list_parser = subparsers.add_parser('list', help='List albums')
    list_parser.add_argument('--album', help='Name of the album')

     # Команда delete
    delete_parser = subparsers.add_parser('delete', help='Delete album')
    delete_parser.add_argument('--album', required=True, help='Name of the album')
    delete_parser.add_argument('--photo', help='Photo')

    # Команда mksite
    mksite_parser = subparsers.add_parser('mksite', help='Generate and publish photo archive website')
    
    # Команда init
    init_parser = subparsers.add_parser('init', help='Initialize the program')
    
    args = parser.parse_args()

    if args.command == 'upload':
        if args.album:
            album = args.album
            photos_dir = args.path if args.path else "."
            upload_photos(album, photos_dir)
        else:
            parser.print_help()

    elif args.command == 'download':
        if args.album:
            album = args.album
            photos_dir = args.path if args.path else "."
            download_photos(album, photos_dir)
        else:
            parser.print_help()

    elif args.command == 'list':
        if args.album:
            album = args.album 
            list_photos(album)
        else:
            list_albums()
        
    elif args.command == 'delete':
        if args.album :
            album = args.album
            photo = args.photo
            delete_photos(album, photo)
        else:
            parser.print_help()

    elif args.command == 'mksite':
        mksite()
    elif args.command == 'init':
        initialize()
    else:
        parser.print_help()
    

if __name__ == "__main__":
    main()