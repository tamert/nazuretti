import flask
import Image

import os
from os.path import isfile

from flask import json, request, url_for
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads
from flask.ext.wtf import Form, FileField, file_allowed, file_required, HiddenField, TextField, TextAreaField, widgets
from werkzeug import secure_filename 

import models

images = UploadSet('imagse', IMAGES, default_dest=lambda x: flask.current_app.config['UPLOAD_FOLDER'])
configure_uploads(flask.current_app, (images,))

class FileUploadWidget(widgets.FileInput):
  def __call__(self, field, **kwargs):
    kwargs['data-url'] = '/admin/mirrorimage/'

    return super(FileUploadWidget, self).__call__(field, **kwargs)

class ProductForm(Form):
  title = TextField('Isim')
  description = TextAreaField("Kisa Metin")
  photo = FileField("Fotograf", widget=FileUploadWidget())

  def validate_photo(form, field):
    if field.data:
      field.data = secure_filename(field.data.filename)
    else:
      field.data = ''

class ProductView(ModelView):
  edit_template   = 'admin/products/edit.html'
  create_template = 'admin/products/create.html'
  form = ProductForm

  def __init__(self, session, **kwargs):
    super(ProductView, self).__init__(models.Product, session, **kwargs)

  def process_image(self, form, model):
    if request.form['image-0']:
      uploadFolder = flask.current_app.config['UPLOAD_FOLDER']
      mirrorPath   = os.path.join(uploadFolder, 'mirror', request.form['image-0'])
      newPath      = os.path.join(uploadFolder, request.form['image-0'])
      box = (
        int(request.form['image-0x'], 10),
        int(request.form['image-0y'], 10),
        int(request.form['image-0w'], 10),
        int(request.form['image-0h'], 10)
      )

      img = Image.open(mirrorPath)
      img.crop(box)
      img.save(newPath)

      if model.photo:
        oldpath = os.path.join(flask.current_app.config['UPLOAD_PATH'], model.photo)
        if isfile(oldpath):
          os.remove(oldpath)

      model.photo = request.form['image-0']
      models.db.session.add(model)
      models.db.session.commit()

      if isfile(mirrorPath):
        os.remove(mirrorPath)

  def on_model_change(self, form, model):
    self.process_image(form, model)

  def on_model_delete(self, model):
    file_path = images.path(model.photo)
    if isfile(file_path):
      os.remove(file_path)

class MirrorImage(BaseView):
  @expose('/', methods=('POST',))
  def index(self):
    file = request.files['photo']
    filename = secure_filename(file.filename)
    file.save(os.path.join(os.path.join(flask.current_app.config['UPLOAD_FOLDER'], 'mirror'), filename))
    return json.jsonify(
        url=url_for('static', filename='uploads/mirror/' + filename),
        filename = filename
        )

  def is_visible(self):
    return False


admin = Admin(flask.current_app)
admin.add_view(ModelView(models.Page, models.db.session))
admin.add_view(ProductView(models.db.session))
admin.add_view(MirrorImage())

