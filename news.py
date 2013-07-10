import flask

from flask import request
from models import News

app = flask.current_app

@app.before_request
def load_news():
  news = News.query.limit(10).all()
  request.news = news

