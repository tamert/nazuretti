import os
import flask

from flask import render_template, request, session
from flask.ext.mail import Mail

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.realpath(__file__)) + '/static/uploads/'
app.config['UPLOAD_BASE_URL'] = 'uploads/'
app.config['UPLOAD_MIRROR_URL'] = '/admin/mirrorimage/'
app.config['SECRET_KEY']    = 'dsfhadkjfgnfavkrniu4yi2y348734'
app.config['ENV']   = os.environ.get('LAZUTTI', 'development').lower()
app.debug = True

Mail(app)

flask.current_app = app

from models import *

# import pages/modules
import admin
import news
import orders
import contact
import pictures

@app.route('/')
def index():
  return render_template('pages/index.html')

@app.route('/kahvaltiliklar')
def products():
  products = Product.query.all()
  return render_template('products/index.html', products = products)

if __name__ == "__main__":
  app.run(port=3030)
