import os, re
from slugify import slugify
from dotenv import load_dotenv
import fnmatch
import time
import cv2
import inspect
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) # adds support for importing scripts from inside a parent folder.
from providers.anilist import get_anime_info
load_dotenv()

FOLDERS=[]

def get_media_files_count(dir_entry):
    """Get amount of episodes.
    """
    count = 0
    for entry in os.listdir(dir_entry):
        if (entry).endswith(('.mkv', '.mp4')):
            count += 1
    return count

def get_folders():
    """
    {
        name
        path (fullpath to folder)
        episodes_count
    }
    """
    folders = []
    for f in os.scandir(os.getenv('MEDIA_PATH')):
        if f.is_dir():
            folders.append(dict(name=re.sub("[\(\[].*?[\)\]]", "", f.name).strip(), path=f.path, episodes=get_media_files_count(f), stats=f.stat))
    return folders

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

# ALTERNATIVE

#  for root, dirs, files in os.walk(directory):
        # print(root)
        # for file in files:
            # if(file.endswith(".mkv")):
                # f = open(os.path.join(root,file)).read()
                # metadata, markdown = frontmatter.parse(f)
                # markup = styleHandler(markdown2.markdown(markdown, extras=['fenced-code-blocks', 'smarty-pants', 'spoiler', 'tables', 'task_list']))
                # if not len(metadata) == 0: # Check if article has metadata at all. If not, do not proceed.
                    # metadata['slug'] = slugify(metadata['title'])
                    # if metadata['publish']:
                        # videos.append(Article(metadata, markup))

FOLDERS = get_folders()

if __name__ == '__main__':

    generate_preview_thumb(os.getenv('EXAMPLE_VIDEO_FOLDER_PATH'), './nekomedia/static/thumbs')

    # FOLDERS = get_folders()
    # for f in FOLDERS:
        # print(f)