from .imports import *

class IndexView(AdminIndexView):
  @expose('/')
  def index(self):
    return self.render('admin/index/index.html')

class SiteSettingsView(BaseView):
  @expose('/', methods=('GET',))
  def index(self):
    settings = {}
    return self.render('admin/site_settings/form.html', settings=settings)
