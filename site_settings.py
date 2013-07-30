import flask
import models
from flask import _request_ctx_stack

@flask.current_app.before_request
def before_request():
  flask.g.site_settings = models.SiteSettings.query.get(1)
