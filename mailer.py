import flask
from flask.ext.mail import Mail, Message

app = flask.current_app
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'umurgdk@gmail.com'
app.config['MAIL_PASSWORD'] = 'xiackok1u9m9u1r'

mail = Mail(app)

def message(**kwargs):
  return Message(**kwargs)

def connect(**kwargs):
  return mail.connect(**kwargs)

