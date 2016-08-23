from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/journal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["SECRET_KEY"] =  os.environ.get('SECRET')


db = SQLAlchemy(app)

#models
class User(db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text(), nullable=False, unique=True)
  # lazy dynamic allows you to do more complex queries
  entries = db.relationship('Journal', backref='user', lazy='dynamic')

  def __init__(self, username):
    self.username = username




class Journal(db.Model):

  __tablename__ = 'entries'

  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.Text(), nullable=False)
  time_created = db.Column(db.TIMESTAMP(timezone=False))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  def __init__(self,text, user_id, time_created):
    self.text = text
    self.user_id = user_id
    self.time_created

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run(debug=True, port=5000)