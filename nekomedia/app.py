from flask import Flask, render_template, redirect, url_for
import sys
from flask_frozen import Freezer
from slugify import slugify

app = Flask(__name__)

@app.template_filter()
def _slugify(text):
    return slugify(text)

@app.route('/')
def hello():
    return render_template('index.html', categories=[])

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