from jinja2 import Environment, FileSystemLoader
from json import load
import json
import os
cwd = os.getcwd()
template_env = Environment(loader=FileSystemLoader(searchpath='D:/Open-Source/Neko Media/src/frontend/template/'))
template = template_env.get_template('template.html')

def get_data():
    with open('D:/Open-Source/Neko Media/src/frontend/template/mock.json', 'r') as data_file:
        return json.load(data_file)

def generate():
    data = get_data()
    with open('D:/Open-Source/Neko Media/src/frontend/public/index.html', 'w') as output_file:
        output_file.write(
            template.render(
                title=data['title'],
                thumbnail='file:///' + data['thumbnail_path'],
                episodes=data['episodes'],
            )
        )

generate()

# file:///