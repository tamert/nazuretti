import flask
import Image

import os
from os.path import isfile

from flask import json, request, url_for
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads
from flask.ext.wtf import Form, FileField, file_allowed, file_required, HiddenField, TextField, TextAreaField, widgets
from wtforms.widgets import core as wtf
from werkzeug import secure_filename 

import models

images = UploadSet('imagse', IMAGES, default_dest=lambda x: flask.current_app.config['UPLOAD_FOLDER'])
configure_uploads(flask.current_app, (images,))

class FileUploadWidget(widgets.FileInput):
  def __call__(self, field, **kwargs):
    kwargs['data-url'] = '/admin/mirrorimage/'

    html = super(FileUploadWidget, self).__call__(field, **kwargs)
    if field.data != '':
      params = dict(
        name  = '%s-old' % (field.name),
        value = field.data,
        type  = 'hidden'
      )
      html += wtf.HTMLString(u'<input %s>' % wtf.html_params(**params))

    return html

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
        int(float(request.form['image-0x'])),
        int(float(request.form['image-0y'])),
        int(float(request.form['image-0x2'])),
        int(float(request.form['image-0y2']))
      )

      img = Image.open(mirrorPath)
      img = img.crop(box)
      img.save(newPath)

      model.photo = request.form['image-0']
      models.db.session.add(model)
      models.db.session.commit()

      if isfile(mirrorPath):
        os.remove(mirrorPath)
      if model and hasattr(model, 'id') and model.id > 0:
        if request.form['photo-old']:
          oldphoto = request.form['photo-old']
          oldpath = os.path.join(flask.current_app.config['UPLOAD_FOLDER'], oldphoto)

          if isfile(oldpath):
            os.remove(oldpath)

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

    img = Image.open(os.path.join(os.path.join(flask.current_app.config['UPLOAD_FOLDER'], 'mirror'), filename))
    width, height = img.size

    return json.jsonify(
      url=url_for('static', filename='uploads/mirror/' + filename),
      filename = filename,
      size=dict(width=width, height=height)
    )

  def is_visible(self):
    return False


admin = Admin(flask.current_app)
admin.add_view(ModelView(models.Page, models.db.session))
admin.add_view(ProductView(models.db.session))
admin.add_view(MirrorImage())

