import os
import errno

def write_to_file(json):
    with codecs.open('result.json', 'w', 'utf-8') as f:
        f.write(json)

def path_model(path):
    model = {
        # 'type': 'folder',
        'name': os.path.basename(path),
        'path': path,
    }

    try:
        model['children'] = [
            path_model(os.path.join(path, contents))
            for contents in os.listdir(path)
        ]
    except OSError as e:
        if e.errno != errno.ENOTDIR: # If found a file then
            raise
        model['type'] = 'episode' # update type to "file"

    return model

if __name__ == '__main__':
    import json
    import sys
    import codecs

    try:
        directory = "./src/test-dir/SERIES"
        # directory = sys.argv[1]
    except IndexError:
        directory = "."

    result = json.dumps(path_model(directory), indent=1, sort_keys=True, ensure_ascii=False)
    print(result)
    write_to_file(result)

