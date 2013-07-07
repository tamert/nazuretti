import flask

from flask import render_template, request, session
from flask.ext.babelex import Babel

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads/'
app.config['SECRET_KEY'] = 'dsfhadkjfgnfavkrniu4yi2y348734'
app.debug = True

flask.current_app = app

import localize
from models import *
import admin

@app.route('/')
def index():
  return render_template('pages/index.html')

@app.route('/kahvaltiliklar')
def products():
  products = Product.query.all()
  return render_template('products/index.html', products = products)

@app.route('/siparis', methods=('GET', ))
def orders():
  products = Product.query.filter(Product.is_orderable == True)
  orders   = session['orders'].values() if session.has_key('orders') else []
  shopping_cart = dict(orders = [], total = 27)
  return render_template('products/order_list.html', products = products, orders = orders)

@app.route('/add-to-cart', methods=('POST', ))
def add_to_card():
  row2dict = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns}
   
  if request.form.has_key('product_id'):
    productId = int(request.form['product_id'], 10)
    product = Product.query.get(productId)

    if product and product.is_orderable:
      if session.has_key('orders'):
        orders = session['orders']
      else:
        orders = {}

      if orders.has_key(str(product.id)):
        order = orders[str(product.id)]

        if request.form.has_key('dec'):
          order['quantity'] -= 1
        else:
          order['quantity'] += 1

        order['total'] = float(product.price) * order['quantity']
          
        
      else:
        orders[str(product.id)] = dict(
          product  = row2dict(product),
          total    = product.price,
          quantity = 1
        )

      session['orders'] = orders
      
      return flask.jsonify(success=True, order=orders[str(product.id)])

  return flask.jsonify(success=False)

@app.route('/remove-from-cart', methods=('POST', ))
def remove_from_cart():
  row2dict = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns}
   
  if request.form.has_key('product_id'):
    productId = int(request.form['product_id'], 10)
    product = Product.query.get(productId)

    if product and product.is_orderable:
      if session.has_key('orders'):
        orders = session['orders']

        if orders.has_key(str(product.id)):
          del orders[str(product.id)]
          session['orders'] = orders
        
          return flask.jsonify(success=True)

  return flask.jsonify(success=False)


if __name__ == "__main__":
  app.run(port=3000)
