from .imports import *
from .utilities import *
from .fields import FileUploadField

from flask.ext.wtf import BooleanField, FloatField, Optional

class ProductForm(Form):
  title = TextField('Isim')
  description = TextAreaField("Kisa Metin")
  photo = FileUploadField("Fotograf")
  is_orderable = BooleanField("Siparis Verilebilir?")
  price = FloatField("Fiyat", validators=[Optional()])
  quantity = TextField("Miktar", validators=[Optional()])

class ProductView(ModelView):
  list_template   = 'admin/products/list.html'
  edit_template   = 'admin/products/edit.html'
  create_template = 'admin/products/create.html'
  form = ProductForm
  column_formatters = dict(
    photo=photo_formatter
  )
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

  def process_image(self, form, model):
    if request.form.has_key('image-0'):
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
      width, height = img.size
      if width != 260 or height != 150:
        img.thumbnail((260, 150), Image.ANTIALIAS)
      img.save(newPath, quality=100)

      model.photo = request.form['image-0']
      models.db.session.add(model)
      models.db.session.commit()

      if isfile(mirrorPath):
        os.remove(mirrorPath)

      if model and hasattr(model, 'id') and model.id > 0:
        if request.form.has_key('photo-old') and request.form['photo-old'] != request.form['image-0']:
          oldphoto = request.form['photo-old']
          oldpath = os.path.join(flask.current_app.config['UPLOAD_FOLDER'], oldphoto)

          if isfile(oldpath):
            os.remove(oldpath)

  def on_model_change(self, form, model):
    if request.form.has_key('image-0'):
      self.process_image(form, model)
    elif request.form.has_key('old-photo'):
      model.photo = request.form['old-photo']

  def on_model_delete(self, model):
    file_path = os.path.join(flask.current_app.config['UPLOAD_FOLDER'], 'uploads', model.photo)
    if isfile(file_path):
      os.remove(file_path)

