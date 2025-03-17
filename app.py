from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

def load_blog_posts():
    """Reads the blog posts from the JSON file."""
    with open("blogposts.json", "r") as fileobj:
        return json.load(fileobj)


def save_blog_posts(posts):
    """Writes the updated list of blog posts to the JSON file."""
    with open("blogposts.json", "w") as fileobj:
        json.dump(posts, fileobj, indent=4)


@app.route('/')
def index():
    """Render the homepage with all blog posts."""
    posts = load_blog_posts()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Handles adding a new blog post."""
    if request.method == 'POST':
        blog_posts = load_blog_posts()

        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        max_id = 0
        for book_data in blog_posts:
            if max_id < book_data["id"]:
                max_id = book_data["id"]

        id_new_post = max_id + 1

        new_post = {
            "id": id_new_post,
            "author": author,
            "title": title,
            "content": content
        }

        blog_posts.append(new_post)
        save_blog_posts(blog_posts)

        return redirect('/')

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Deletes a blog post by ID and redirects to the homepage."""
    blog_posts = load_blog_posts()

    updated_blog_posts = []
    for post in blog_posts:
        if post["id"] != post_id:
            updated_blog_posts.append(post)

    save_blog_posts(updated_blog_posts)

    return redirect('/')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Handles updating a blog post."""
    blog_posts = load_blog_posts()

    post_to_edit = None
    for post in blog_posts:
        if post["id"] == post_id:
            post_to_edit = post
            break

    if post_to_edit is None:
        return "Post not found", 404

    if request.method == 'POST':
        post_to_edit["author"] = request.form.get("author")
        post_to_edit["title"] = request.form.get("title")
        post_to_edit["content"] = request.form.get("content")
        save_blog_posts(blog_posts)

        return redirect('/')

    return render_template('update.html', post=post_to_edit)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)