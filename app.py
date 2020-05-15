from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import os
#import tornado.ioloop
#import tornado.web

#file_path = os.path.abspath(os.getcwd())+"\blog.db"

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'blog.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)

class member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route('/HOME')
def index():
    posts =member.query.order_by(member.date_posted.desc()).all()
    return render_template('index.html',posts=posts)

@app.route('/ABOUT')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = member.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/CONTACT')
def contact():
    return render_template('Contact.html')

@app.route('/addpost' ,methods=['GET','POST'])
def addpost():
    if request.method=='POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        author = request.form['author']
        content = request.form['content']
        post = member(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('index.html')

@app.route('/delete', methods=('GET','POST',))
def delete(post_id):
    if request.method=="POST":
        if post_id:
        get_post(post_id)
        db = get_db(post_id)
        db.execute('DELETE FROM post WHERE id = ?', (post_id))
        db.commit()
        return redirect(url_for('index.html'))
        else:
            return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    #app.listen(8888)
    #tornado.ioloop.IOLoop.current().start()

