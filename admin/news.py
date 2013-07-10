from .imports import *
from .utilities import *

from datetime import date

from models import db

class NewsForm(Form):
  content = TextAreaField('Haber')


class NewsView(ModelView):
  list_template = 'admin/news/list.html'
  form = NewsForm
  column_labels = dict(content='Haber', created_at='Tarih')

  column_formatters = dict(
    created_at = lambda v, c, m, p: m.created_at.strftime('%d/%m/%Y')
  )

  form_widget_args = dict(
    content = dict(
      rows=5,
      cols=80,
      style='width: 100%;'
    )
  )

  def __init__(self, session, **kwargs):
    super(NewsView, self).__init__(models.News, session, **kwargs)

  def on_model_change(self, form, model):
    if model.id == None:
      model.created_at = date.today()

