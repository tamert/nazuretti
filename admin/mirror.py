from .imports import *

class MirrorImage(BaseView):
  @expose('/', methods=('POST',))
  def index(self):
    file = request.files['photo']
    filename = secure_filename(file.filename)
    filepath = os.path.join(os.path.join(flask.current_app.config['UPLOAD_FOLDER'], 'mirror'), filename)

    img = Image.open(file)
    img.save(filepath, quality=100)
    width, height = img.size

    return json.jsonify(
      url=url_for('static', filename='uploads/mirror/' + filename),
      filename = filename,
      size=dict(width=width, height=height)
    )

  @expose('/clean/', methods=('POST', ))
  def clean(self):
    filename = request.form['filename']

    parts = filter(lambda x: x != '', filename.split('/'))
    filename = parts[-1]
    path = os.path.join(flask.current_app.config['UPLOAD_FOLDER'], 'mirror', filename)

    if isfile(path):
      os.remove(path)

    return json.jsonify(success=True)

  def is_visible(self):
    return False

