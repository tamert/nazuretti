from .imports import *
from flask import url_for, redirect

class IndexView(AdminIndexView):
  @expose('/')
  def index(self):
    return self.render('admin/index/index.html')

class SiteSettingsForm(Form):
  facebook      = TextField('Facebook Adresi')
  twitter       = TextField('Twitter Adresi')

  order_email   = TextField('Siparis Email')
  order_phone   = TextField('Siparis Telefon')

  contact_email = TextField('Iletisim Email')
  contact_phone = TextField('Iletisim Telefon')

  bank_person   = TextField('Banka Alici Ismi')
  bank_name     = TextField('Banka Ismi')
  bank_iban     = TextField('Banka IBAN')


class SiteSettingsView(BaseView):
  @expose('/', methods=('GET',))
  def index(self):
    settings = models.SiteSettings.query.all()

    if len(settings) == 0:
      raise "SiteSetting shouldn't be empty"

    form = SiteSettingsForm(obj=settings[0])

    return self.render('admin/site_settings/form.html', form=form)

  @expose('/', methods=('POST',))
  def update(self):
    settings = models.SiteSettings.query.get(1)

    if not settings:
      raise "SiteSetting shouldn't be empty"

    form = SiteSettingsForm(request.form)
    form.populate_obj(settings)

    models.db.session.add(settings)
    models.db.session.commit()

    return redirect(url_for('sitesettings.index'))
