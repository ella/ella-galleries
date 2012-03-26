from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.translation import ungettext
from django.utils.cache import patch_vary_headers

from ella.core.views import get_templates_from_publishable
from ella.core.signals import object_rendered

def gallery_item_detail(request, context, item_slug=None):
    '''
    Returns ``GalleryItem`` object by its slug or first one (given by
    ``GalleryItem``.``order``) from ``Gallery``.
    '''
    gallery = context['object']
    item_sorted_dict = gallery.items
    count = len(item_sorted_dict)
    count_str = ungettext('%(count)d object total', '%(count)d objects total',
        count) % {'count': count}
    next = None
    previous = None

    if count == 0:
        # TODO: log empty gallery
        raise Http404()

    if item_slug is None:
        item = item_sorted_dict.value_for_index(0)
        if count > 1:
            next = item_sorted_dict.value_for_index(1)
        position = 1
    else:
        try:
            item = item_sorted_dict[item_slug]
        except KeyError:
            raise Http404()
        item_index = item_sorted_dict.keyOrder.index(item_slug)
        if item_index > 0:
            previous = item_sorted_dict.value_for_index(item_index - 1)
        if (item_index + 1) < count:
            next = item_sorted_dict.value_for_index(item_index + 1)
        position = item_index + 1


    context.update({
        'gallery': gallery,
        'item': item,
        'item_list' : item_sorted_dict.values(),
        'next' : next,
        'previous' : previous,
        'count' : count,
        'count_str' : count_str,
        'position' : position,
    })

    if request.is_ajax():
        template_name = "item-ajax.html"
    else:
        template_name = "item.html"

    response = TemplateResponse(
        request,
        get_templates_from_publishable(template_name, context['object']),
        context,
    )
    object_rendered.send(sender=context['object'].__class__, request=request, category=context['category'], publishable=context['object'])

    patch_vary_headers(response, ('X-Requested-With',))
    return response

