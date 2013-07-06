import flask
from flask import current_app, session, request
from flask.ext.babelex import Babel

babel = Babel(current_app)

@babel.localeselector
def get_locale():
  override = request.args.get('lang')

  if override:
    session['lang'] = override

  return session.get('lang', 'tr')
