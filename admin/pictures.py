from .imports import *
from .utilities import *
from .fields import FileUploadField

from flask.ext.wtf import BooleanField, FloatField, Optional
from models import db

from components.image import Image as ImageKit

class PictureForm(Form):
  title = TextField('Isim')
  image = FileUploadField("Resim")

class PictureView(ModelView):
  list_template   = 'admin/pictures/list.html'
  edit_template   = 'admin/pictures/edit.html'
  create_template = 'admin/pictures/create.html'
  form = PictureForm
  column_formatters = dict(
    image=photo_formatter
  )
  column_labels = dict(
    title        = 'Isim',
    image        = 'Resim',
  )

  def __init__(self, session, **kwargs):
    super(PictureView, self).__init__(models.Picture, session, **kwargs)

  def process_image(self, form, model):
    if request.form.has_key('image-0'):
      newfilename  = request.form['image-0']
      uploadFolder = flask.current_app.config['UPLOAD_FOLDER']
      mirrorPath   = os.path.join(uploadFolder, 'mirror', request.form['image-0'])
      newPath      = os.path.join(uploadFolder, 'pictures', newfilename)
      thumbPath    = os.path.join(uploadFolder, 'pictures', 'thumbs', newfilename)
      box = (
        int(float(request.form['image-0x'])),
        int(float(request.form['image-0y'])),
        int(float(request.form['image-0x2'])),
        int(float(request.form['image-0y2']))
      )

      img = ImageKit(mirrorPath)
      img.crop(box)
      img.resize((1024, 600))
      img.save(newPath)

      thumb = ImageKit(newPath)
      thumb.thumbnail((260, 150))
      thumb.save(thumbPath)

      model.image = newfilename
      models.db.session.add(model)
      models.db.session.commit()

      if isfile(mirrorPath):
        os.remove(mirrorPath)

      if model and hasattr(model, 'id') and model.id > 0:
        if request.form.has_key('image-old') and request.form['image-old'] != newfilename:
          oldphoto = request.form['image-old']
          oldpath = os.path.join(uploadFolder, 'pictures', oldphoto)

          if isfile(oldpath):
            os.remove(oldpath)

  def on_model_change(self, form, model):
    if request.form.has_key('image-0'):
      self.process_image(form, model)
    elif request.form.has_key('image-old'):
      model.image = request.form['image-old']

  def after_model_change(self, form, model, created):
    if model.image:
      base_path = os.path.join(flask.current_app.config['UPLOAD_FOLDER'], 'pictures')
      path = os.path.join(base_path, model.image)

      image = str(model.id) + '_' + model.image
      new_path = os.path.join(base_path, image)

      thumbPath = os.path.join(base_path, 'thumbs', model.image)
      newThumbPath = os.path.join(base_path, 'thumbs', image)
      if isfile(path):
        os.rename(path, new_path)
        model.image = image
        db.session.add(model)
        db.session.commit()

      if isfile(thumbPath):
        os.rename(thumbPath, newThumbPath)


  def on_model_delete(self, model):
    base_path  = os.path.join(flask.current_app.config['UPLOAD_FOLDER'], 'pictures')
    file_path  = os.path.join(base_path, model.image)
    thumb_path = os.path.join(base_path, 'thumbs', model.image)

    if isfile(file_path):
      os.remove(file_path)

    if isfile(thumb_path):
      os.remove(thumb_path)


