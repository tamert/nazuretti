import flask

from flask import render_template, request, session, abort, flash
from flask.ext.mail import Mail

from models import Product
import mailer

app = flask.current_app

@app.route('/siparis', methods=('GET', ))
def orders():
  products = Product.query.filter(Product.is_orderable == True)
  orders   = session['orders'].values() if session.has_key('orders') else []

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

@app.route('/submit-order', methods=('POST',))
def submit_order():
  name    = request.form.get('name', '')
  email   = request.form.get('email', '')
  phone   = request.form.get('phone', '')
  city    = request.form.get('city', '')
  address = request.form.get('address', '')
  message = request.form.get('message', '')

  required_fields = [name, email, phone, city, address]
  if not all([x != '' for x in required_fields]):
    return abort(404)

  orders = session.get('orders', {}).values()
  total  = reduce(lambda total, x: total + float(x['total']), orders, 0)

  customer = dict(
    name=name,
    email=email,
    phone=phone,
    city=city,
    address=address,
    message=message
  )

  mail_body = render_template('mails/new_order.html', orders=orders, customer=customer, total=total)
  with mailer.connect() as con:
    msg = mailer.message(recipients=[app.config['ORDER_RECEIVER']],
                         html=mail_body,
                         subject='Siparis Var!',
                         sender=app.config['ORDER_SENDER'])
    con.send(msg)

  session['orders'] = {}
  return render_template('products/order_thankyou.html', orders=orders, total=total)
