from .imports import *

import os
from os.path import isdir

class MirrorImage(BaseView):
  @expose('/', methods=('POST',))
  def index(self):
    file = request.files.values().pop()
    upload_folder = flask.current_app.config['UPLOAD_FOLDER']
    upload_base_url = flask.current_app.config.get('UPLOAD_BASE_URL', '')
    filename = secure_filename(file.filename)
    model_name = request.form.get('model_name', None)

    if model_name:
      dirpath  = os.path.join(upload_folder, 'mirror', model_name)
      url      = upload_base_url + 'mirror/' + model_name + '/' + filename
    else:
      dirpath  = os.path.join(upload_folder, 'mirror')
      url      = upload_base_url + 'mirror/' + filename

    filepath = os.path.join(dirpath, filename)

    if not isdir(dirpath):
      os.mkdir(dirpath)

    img = Image.open(file)
    img.save(filepath, quality=100)
    width, height = img.size

    return json.jsonify(
      url=url_for('static', filename=url),
      filename = filename,
      size=dict(width=width, height=height)
    )

  @expose('/clean/', methods=('POST', ))
  def clean(self):
    upload_folder = flask.current_app.config['UPLOAD_FOLDER'] 
    filename = request.form['filename']

    parts = filter(lambda x: x != '', filename.split('/'))
    filename = parts[-1]
    model_name = request.form.get('model_name', None)

    if model_name:
      dirpath  = os.path.join(upload_folder, 'mirror', model_name)
      filepath = os.path.join(dirpath, filename)
    else:
      dirpath  = os.path.join(upload_folder, 'mirror')
      filepath = os.path.join(dirpath, filename)

    if isfile(filepath):
      os.remove(filepath)

    return json.jsonify(success=True)

  def is_visible(self):
    return False

