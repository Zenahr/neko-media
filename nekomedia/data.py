import os, re
from slugify import slugify
from dotenv import load_dotenv

load_dotenv()

FOLDERS=[]

def get_folders():
    """
    {
        name
        episodes_count
    }
    """
    first_level_folder_names = [ re.sub("[\(\[].*?[\)\]]", "", name).strip() for name in os.listdir(os.getenv('MEDIA_PATH')) if os.path.isdir(os.path.join(os.getenv('MEDIA_PATH'), name)) ]
    # full_path_to_first_level_folders = [f.path for f in os.scandir(os.getenv('MEDIA_PATH')) if f.is_dir()] # get fullpath to first level folders only.
    return [dict(name=folder) for folder in first_level_folder_names]

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
    FOLDERS = get_folders()
    for f in FOLDERS:
        print(f)