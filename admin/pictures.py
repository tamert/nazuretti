from .imports import *
from .utilities import *

from .components.image_upload.fields import ImageUploadField

from flask.ext.wtf import BooleanField, FloatField, Optional
from models import db

from .components.image_upload.image import Image as ImageKit
from .components.image_upload.image_upload import get_image_column_formatter, add_image_uploading_handlers


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
    super(PictureView, self).__init__(models.Picture, session, **kwargs)
    self.column_formatters['image'] = get_image_column_formatter(self.form.image, 'image')
    add_image_uploading_handlers(self.form, self.model, session, self)
