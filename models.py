import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import url_for
from flask import Markup

app = flask.current_app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lazutti.db'
app.config['SQLALCHEMY_ECHO']         = True

db = SQLAlchemy(app)

class Page(db.Model):
  __tablename__ = 'pages'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, unique=True)
  content = db.Column(db.String)

  def __unicode__(self):
    return u'<Page:%s>' % (self.title)

class Product(db.Model):
  __tablename__ = 'products'

  id           = db.Column(db.Integer, primary_key = True)
  title        = db.Column(db.String)
  description  = db.Column(db.Text)
  photo        = db.Column(db.String)
  is_orderable = db.Column(db.Boolean)
  price        = db.Column(db.String)
  quantity     = db.Column(db.String)

  def thumbnail(self):
    url = url_for('static', filename='uploads/' + self.photo)
    return Markup(u'<img src="%s" />' % url)

  def __unicode__(self):
    return u'<Product:%s>' % (self.title)

class Picture(db.Model):
  __tablename__ = 'pictures'

  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String)
  description = db.Column(db.Text)
  image = db.Column(db.String)

  def thumbnail(self):
    url = url_for('static', filename='uploads/pictures')
    return Markup(u'<img src="%s" />' % url)

  def __unicode__(self):
    return u'<Picture:%s>' % self.image

class News(db.Model):
  __tablename__ = 'news'

  id = db.Column(db.Integer, primary_key = True)
  content = db.Column(db.Text)
  created_at = db.Column(db.Date)

  def __unicode__(self):
    return u'<News:%s...>' % self.content[0:10]
