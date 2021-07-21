import os, re
from slugify import slugify
from dotenv import load_dotenv
import fnmatch
import time
import cv2
import inspect
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # https://stackoverflow.com/a/11158224/12675239 Adds support for importing scripts from inside a parent folder. PYTHONPATH env var.
from providers.anilist import get_anime_info
load_dotenv()
import os.path
import urllib.request
import json
import pickle

def flatten(input):
    """flatten recursively. https://www.geeksforgeeks.org/python-program-to-flatten-a-nested-list-using-recursion/"""
    if not(bool(input)):
        return input
    if isinstance(input[0], list):
        return flatten(*input[:1]) + flatten(input[1:])
    return input[:1] + flatten(input[1:])

def get_media_files_count(dir_entry):
    """Get amount of episodes.
    """
    count = 0
    for entry in os.listdir(dir_entry):
        if (entry).endswith(('.mkv', '.mp4')):
            count += 1
    return count

def get_folders(base_folder=os.getenv('MEDIA_PATH')):
    """
    {
        name
        path (fullpath to folder)
        episodes_count
    }
    """
    folders = []
    for f in os.scandir(base_folder):
        print('added', len(folders), 'anime')
        if f.is_dir():
            name = re.sub("[\(\[].*?[\)\]]", "", f.name).strip()
            info = get_anime_info(name)
            thumb = ''
            try:
                thumb = info['thumb']
            except KeyError:
                continue
            folders.append(dict(
                name=name,
                path=f.path,
                episodes=get_media_files_count(f),
                # stats=f.stat,
                thumb=info['thumb'],
                info=info['info']
                    )
                )
    return flatten(folders)

def get_all_folders():
    """infinitely recursive version of get_folders()"""
    try:
        if pickle.load(open("data.p", "rb")):
                return pickle.load(open("data.p", "rb"))
    except EOFError:
        print('corrupted data or never cached before.')
        result = []
        for root, dirs, files in os.walk(os.getenv('MEDIA_PATH')):
            for filename in files:
                # print(os.path.join(root, filename))
                pass
            for dirname in dirs:
                # print(os.path.join(root, dirname))
                print(f'scanning dir: {dirname}')
                temp = get_folders(os.path.join(root, dirname))
                if not temp == []:
                    result.append(temp)
                print('RESULT ---------------------------------------------')
                print(result)
    pickle.dump(flatten(result), open( "data.p", "wb" ) )
    return flatten(result)

def serve_thumb(name):
    # SCRAPPED BECAUSE 403. USE URI'S DIRECTLY INSTEAD.
    '''
    look for image on disk first.
    /static/thumbs/anime name.png
    if you can't find a thumb, fetch the thumb, save it and return the path.
    otherwise just return the path to /static/thumbs/anime name.png
    '''
    img_path = './static/thumbs'
    fname = os.path.join(img_path, name, '.png')
    if not os.path.isfile(os.path.join(fname)):
        try:
            print(f'downloading thumbnail for {name}')
            uri = get_anime_info(name)['thumb']
            urllib.request.urlretrieve(uri, f'{img_path}/{name}.png') # https://stackoverflow.com/a/8286449/12675239
        except urllib.error.HTTPError:
            print('probably HTTP Error 403: Forbidden. Sadge.')
            return ''
    else:
        return f'{img_path}/{name}.png'
        

def generate_preview_thumb(video_files_directory, output_loc='./static/thumbs'):
    """"Credit: https://stackoverflow.com/a/49011190/12675239"""
    # TODO: don't use filename but rather directory name. Makes it easier to create url_for() references to thumbnails later on.
    video_file_name = None
    for entry in os.listdir(video_files_directory):
        if (entry).endswith(('.mkv', '.mp4')):
            video_file_name = entry
            break
    file = os.path.join(video_files_directory, video_file_name)
    try:
        os.mkdir(output_loc)
    except OSError:
        pass
    cap = cv2.VideoCapture(file)
    while cap.isOpened():
        ret, frame = cap.read()
        print(video_files_directory)
        thumb_name = video_files_directory.rsplit('\\', 1)[-1].strip() # Seperate directory name from parent folder.
        cv2.imwrite(output_loc + f"/{thumb_name}.jpg", frame)
        break # we only need ONE image per video for our preview.

    # first_level_folder_names = [ re.sub("[\(\[].*?[\)\]]", "", name).strip() for name in os.listdir(os.getenv('MEDIA_PATH')) if os.path.isdir(os.path.join(os.getenv('MEDIA_PATH'), name)) ]
    # full_path_to_first_level_folders = [f.path for f in os.scandir(os.getenv('MEDIA_PATH')) if f.is_dir()] # get fullpath to first level folders only.
    # print(full_path_to_first_level_folders)
    # return [dict(name=re.sub("[\(\[].*?[\)\]]", "", folder.rsplit('\\', 1)[-1]).strip(), path=folder) for folder in full_path_to_first_level_folders]

if __name__ == '__main__':
    pass
    # generate_preview_thumb(os.getenv('EXAMPLE_VIDEO_FOLDER_PATH'), './nekomedia/static/thumbs')

    # FOLDERS = get_folders()
    # for f in FOLDERS:
    #     print(f['name'])

    # print(flatten(get_folders()))