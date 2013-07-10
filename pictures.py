import flask

from flask import session, request, render_template
from models import Picture

app = flask.current_app

@app.route('/fotograflar', methods=('GET',))
def pictures():
  pictures = Picture.query.all()

  return render_template('pictures/index.html', pictures=pictures)
