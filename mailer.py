import os

import flask
from flask.ext.mail import Mail, Message

app = flask.current_app

if os.environ['LAZUTTI'] == 'PRODUCTION':
  app.config['MAIL_SERVER'] = 'smtp.webfaction.com'
  app.config['MAIL_USERNAME'] = 'lazutti'
  app.config['MAIL_PASSWORD'] = '123456'

  app.config['ORDER_SENDER'] = 'siparis@lazutti.com'
  app.config['ORDER_RECEIVER'] = 'siparis@lazutti.com'

  app.config['CONTACT_SENDER'] = 'lazutti@lazutti.com'
  app.config['CONTACT_RECEIVER'] = 'lazutti@lazutti.com'

else:
  app.config['MAIL_SERVER'] = 'smtp.gmail.com'
  app.config['MAIL_PORT'] = 465
  app.config['MAIL_USE_SSL'] = True
  app.config['MAIL_USERNAME'] = 'umurgdk@gmail.com'
  app.config['MAIL_PASSWORD'] = 'xiackok1u9m9u1r'

  app.config['ORDER_SENDER'] = 'umurgdk@gmail.com'
  app.config['ORDER_RECEIVER'] = 'umurgdk@gmail.com'

  app.config['CONTACT_SENDER'] = 'umurgdk@gmail.com'
  app.config['CONTACT_RECEIVER'] = 'umurgdk@gmail.com'

mail = Mail(app)

def message(**kwargs):
  return Message(**kwargs)

def connect(**kwargs):
  return mail.connect(**kwargs)

