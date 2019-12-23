from django.conf.urls.defaults import *
import mobileadmin

urlpatterns = patterns('',
    (r'^(.*)', mobileadmin.site.root),
)
