import os
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "build-a-blog.db"))
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'hfdhufbrewbcnoeua'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    body = db.Column(db.String(10000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    posts = Blog.query.filter_by().all()
    return render_template('blog.html', posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    title_error = ''
    body_error = ''

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if empty_string(title):
            title_error = "Please enter a title"
            flash(title_error, 'title_error')
            return render_template('newpost.html', body=body)
        
        if empty_string(body):
            body_error = "Please enter a message"
            flash(body_error, 'body_error')
            return render_template('newpost.html', title=title)
   
        if empty_string(title_error) and empty_string(body_error):
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            post = Blog.query.filter_by(id=new_post.id).first()
            return redirect(f'/blog?id={post.id}')

    return render_template('newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'POST':
        posts = Blog.query.filter_by(title=title).first()
    if request.method == 'GET':
        posts = Blog.query.filter_by().all()
        post_id = request.args.get('id')
        if post_id != None:
            posts = Blog.query.filter_by(id=post_id).first()
    return render_template('blog.html', posts=posts)

#Test if a return value is an empty string
def empty_string(value):
    if(len(value) == 0):
        return True

if __name__ == '__main__':
    app.run()