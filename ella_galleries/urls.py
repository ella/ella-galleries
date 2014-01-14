from django.template.defaultfilters import slugify
from django.utils.translation import ugettext
try:
    from django.conf.urls import patterns, url
except:
    from django.conf.urls.defaults import patterns, url

from ella.core.custom_urls import resolver

from ella_galleries.views import gallery_item_detail
from ella_galleries.models import Gallery

urlpatterns = patterns('',
    url(r'^(?P<item_slug>[\w-]+)/(?P<url_remainder>.+/)$', gallery_item_detail, name='gallery-item-detail-custom'),
    url(r'^(?P<item_slug>[\w-]+)/$', gallery_item_detail, name='gallery-item-detail'),
)

resolver.register(urlpatterns, prefix=slugify(ugettext('Item')), model=Gallery)
resolver.register_custom_detail(Gallery, gallery_item_detail)
