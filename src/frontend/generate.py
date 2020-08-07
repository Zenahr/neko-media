from jinja2 import Environment, FileSystemLoader
from json import load
import json

template_env = Environment(loader=FileSystemLoader(searchpath='./template'))
template = template_env.get_template('template.html')

with open('template/config.json', 'r') as config_file:
    config = json.load(config_file)

with open('public/index.html', 'w') as output_file:
    output_file.write(
        template.render(
            title=config['content']['title'],
            greetingText=config['content']['greetingText'],
            resumeText=config['content']['resumeText'],
            firstName=config['content']['firstName'],
            lastName=config['content']['lastName'],
            github=config['socials']['github'],
            linkedIn=config['socials']['linkedIn'],
            email=config['socials']['email'],
            socialIntroText=config['content']['socialIntroText'],
            closingStatement=config['content']['closingStatement'],
            js=""
        )
    )

file:///