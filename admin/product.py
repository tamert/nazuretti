from .imports import *
from .utilities import *

from flask.ext.wtf import BooleanField, FloatField, Optional
from models import db

from .components.image_upload.fields import ImageUploadField
from .components.image_upload.image_upload import get_image_column_formatter, add_image_uploading_handlers

class ProductForm(Form):
  title = TextField('Isim')
  description = TextAreaField("Kisa Metin")
  photo = ImageUploadField("Fotograf", upload_options=dict(
    crop      = dict(ratio = 260.0 / 150.0, min = (260, 150)),
    max_width = 400,
    resize    = (260,10000000),
    model     = 'products'
  ))
  is_orderable = BooleanField("Siparis Verilebilir?")
  price = FloatField("Fiyat", validators=[Optional()])
  quantity = TextField("Miktar", validators=[Optional()])

class ProductView(ModelView):
  list_template   = 'admin/products/list.html'
  edit_template   = 'admin/products/edit.html'
  create_template = 'admin/products/create.html'
  form = ProductForm
  column_formatters = dict()
  column_labels = dict(
    title        = 'Isim',
    description  = 'Kisa Metin',
    photo        = 'Resim',
    is_orderable = 'Siparis?',
    price        = 'Fiyat',
    quantity     = 'Miktar'
  )

  def __init__(self, session, **kwargs):
    super(ProductView, self).__init__(models.Product, session, **kwargs)
    self.column_formatters['photo'] = get_image_column_formatter(self.form.photo, 'photo')
    add_image_uploading_handlers(self.form, self.model, session, self)
