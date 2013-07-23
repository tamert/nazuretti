from .imports import *
from .utilities import *

from .components.image_upload.fields import ImageUploadField

from flask.ext.wtf import BooleanField, FloatField, Optional
from models import db

from .components.image_upload.image import Image as ImageKit
from .components.image_upload.image_upload import process_image_uploads, update_filenames_to_model, remove_files_after_deletion, get_image_column_formatter

class PictureForm(Form):
  title = TextField('Isim')
  image = ImageUploadField("Resim", upload_options=dict(
    crop       = dict(ratio = 256.0/250.0, min = (256,250)),
    max_width  = 400,
    resize     = (1000, 600),
    thumbnails = [
      dict(name='s', size=(36,36)),
      dict(name='m', size=(100,100))
    ],
    model = 'pictures'
  ))

class PictureView(ModelView):
  list_template   = 'admin/pictures/list.html'
  edit_template   = 'admin/pictures/edit.html'
  create_template = 'admin/pictures/create.html'
  form = PictureForm
  column_formatters = dict()
  column_labels = dict(
    title        = 'Isim',
    image        = 'Resim',
  )

  def __init__(self, session, **kwargs):
    self.column_formatters['image'] = get_image_column_formatter(self.form.image, 'image')
    super(PictureView, self).__init__(models.Picture, session, **kwargs)

  def on_model_change(self, form, model):
    process_image_uploads(form, model, models.db)

  def after_model_change(self, form, model, created):
    update_filenames_to_model(form, model, models.db)

  def on_model_delete(self, model):
    remove_files_after_deletion(self.form, model)

