import flask

from flask import render_template, request
import mailer

app = flask.current_app

@app.route('/iletisim', methods=('GET',))
def contact():
  return render_template('contact/form.html')

@app.route('/iletisim', methods=('POST',))
def contact_submit():
  name    = request.form.get('name', '')
  email   = request.form.get('email', '')
  phone   = request.form.get('phone', '')
  city    = request.form.get('city', '')
  message = request.form.get('message', '')

  required_fields = [name, email, message]
  if not all([x != '' for x in required_fields]):
    return abort(404)

  customer = dict(
    name=name,
    email=email,
    phone=phone,
    city=city,
    message=message
  )

  mail_body = render_template('mails/new_contact.html', customer=customer)
  with mailer.connect() as con:
    msg = mailer.message(recipients=['umurgdk@gmail.com'],
                         html=mail_body,
                         subject='Iletisim Istegi Var!',
                         sender='iletisim@lazutticom')
    con.send(msg)

  return render_template('contact/contact_thankyou.html')
