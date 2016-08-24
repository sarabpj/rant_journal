from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import os


app = Flask(__name__,template_folder='../client/views', static_folder="../client")


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




class Entry(db.Model):

  __tablename__ = 'entries'

  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.Text(), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  time_created = db.Column(db.TIMESTAMP(timezone=False))
  result_text_sentiment = db.Column(JSON)
  result_stop_words = db.Column(JSON)

  def __init__(self,text, user_id, time_created, result_text_sentiment,result_stop_words):
    self.text = text
    self.user_id = user_id
    self.time_created = time_created
    self.result_text_sentiment = result_text_sentiment
    self.result_stop_words = result_stop_words

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/entry')
def new_entry():
    return render_template('index.html')


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)




if __name__ == '__main__':
    app.run(debug=True, port=5000)