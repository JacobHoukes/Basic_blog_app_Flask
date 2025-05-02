import os.path

from flask import Flask, render_template, request, redirect, url_for
import json

blog_posts = [
    {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
    {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'}
]

with open('blog_posts.json', 'w') as file:
    json.dump(blog_posts, file, indent=4)

app = Flask(__name__)


@app.route('/')
def index():
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        if os.path.exists('blog_posts.json'):
            with open("blog_posts.json", "r") as file:
                blog_posts = json.load(file)
        else:
            blog_posts = []

        new_id = max((post['id'] for post in blog_posts), default=0) + 1

        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        blog_posts.append(new_post)
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
