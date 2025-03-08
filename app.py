from flask import Flask, render_template
import json

app = Flask(__name__)

with open("blogposts.json", "r") as fileobj:
    books = json.loads(fileobj.read())

@app.route('/')
def index():
    with open("blogposts.json", "r") as fileobj:
        blog_posts = json.loads(fileobj.read())

    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)