import flask
from flask.ext.sqlalchemy import SQLAlchemy

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

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    photo = db.Column(db.String)

    def __unicode__(self):
        return u'<Product:%s>' % (self.title)

