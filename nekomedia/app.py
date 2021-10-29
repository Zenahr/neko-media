from flask import Flask, render_template, redirect, url_for, request
import sys
from slugify import slugify
from data import get_all_folders, get_folders, flatten
import subprocess
from flask_frozen import Freezer
import os.path
import flaskwebgui

FOLDERS = flatten(get_all_folders())

app = Flask(__name__)
freezer = Freezer(app, with_no_argument_rules=False, log_url_for=False)
gui = flaskwebgui.FlaskUI(app)


@app.template_filter()
def _slugify(text):
    return slugify(text)

@app.route('/')
def index():
    # try:
    #     print('rendering cached version')
    #     return render_template('frozen_index.html') # use cached version if available (AniList images saved).
    # except Exception:
        print('rendering non-cached version')
        return render_template('index.html', categories=FOLDERS)

@freezer.register_generator
def index_generator():
    yield 'index', {'categories': FOLDERS}


@app.route('/open_media_folder')
def open_media_folder():
    path = request.args.get('path').replace('%20', ' ')
    subprocess.run(['explorer.exe', path])
    return redirect(url_for('index'))

# @app.route('/category/<category_slug>')
# def articles(category_slug):
#     data = []
#     for article in []:
#         if slugify(article.metadata['category']) == category_slug:
#             data.append(article)
#     return render_template('category.html', articles=data)

# @app.route('/articles/<slug>')
# def article(slug):
#     for article in []:
#         if article.metadata['slug'] == slug:
#             return render_template('article.html', article=article, thumb=article.metadata['thumb'])
#     return page_not_found(404)

freezer.freeze()
import os
os.replace("nekomedia/build/index.html", "nekomedia/templates/frozen_index.html")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        gui.run()
        # app.run(debug=True)