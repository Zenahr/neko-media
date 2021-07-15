import os, re
from slugify import slugify
from dotenv import load_dotenv
import fnmatch
import time
import cv2

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
    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(file)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", video_length)
    count = 0
    print ("Converting video..\n")
    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        cv2.imwrite(output_loc + f"/{video_file_name}.jpg", frame)
        break # we only need ONE image per video for our preview.
        count = count + 1
        if (count > (video_length-1)):
            time_end = time.time()
            cap.release()
            print ("Done extracting frames.\n%d frames extracted" % count)
            print ("It took %d seconds forconversion." % (time_end-time_start))
            break


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

    generate_preview_thumb('D:\BakaBT\ANIME\Sora yori mo Tooi Basho [BD]', './nekomedia/static/thumbs')

    FOLDERS = get_folders()
    for f in FOLDERS:
        print(f)