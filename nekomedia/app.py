from flask import Flask, render_template, redirect, url_for, request
import sys
from slugify import slugify
from data import get_all_folders, get_folders, flatten
import subprocess

app = Flask(__name__)

FOLDERS = flatten(get_all_folders())

@app.template_filter()
def _slugify(text):
    return slugify(text)

@app.route('/')
def index():
    return render_template('index.html', categories=FOLDERS)

@app.route('/open_media_folder')
def open_media_folder():
    path = request.args.get('path').replace('%20', ' ')
    subprocess.run(['explorer.exe', path])
    return redirect(url_for('index'))

@app.route('/category/<category_slug>')
def articles(category_slug):
    data = []
    for article in []:
        if slugify(article.metadata['category']) == category_slug:
            data.append(article)
    return render_template('category.html', articles=data)

@app.route('/articles/<slug>')
def article(slug):
    for article in []:
        if article.metadata['slug'] == slug:
            return render_template('article.html', article=article, thumb=article.metadata['thumb'])
    return page_not_found(404)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(host='192.168.1.63' ,debug=True)