from flask import Flask, render_template,request, redirect # 追加
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from datetime import datetime,date
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
engine = create_engine(f'sqlite:///todo.db', echo=True)
db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()
        return render_template('index.html', posts=posts,today=date.today())

    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        
        due = datetime.strptime(due, '%Y-%m-%d')
        new_post = Post(title=title, detail=detail, due=due)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/') # 変更
    

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)

    return render_template('detail.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()
        return redirect('/')

@app.route('/result',methods=["GET"])
def result():
    # posts=Post.query.limit(10).all()
    # sql_statement = (
    #                     select([
    #                         User.id,
    #                         User.name, 
    #                         User.age
    #                     ]).filter(
    #                         (User.name == user_name) &
    #                         (User.age >= user_age) 
    #                     ).limit(10)
    #                 )
    sql_statement = 'SELECT * FROM persons limit 10'
    
    df = pd.read_sql_query(sql=sql_statement, con=engine)

    return render_template('dbresult.html',table=(df.to_html(classes="mystyle")))
    # return render_template('dbresult.html',table=posts)


if __name__ == "__main__":
    app.run(debug=True)