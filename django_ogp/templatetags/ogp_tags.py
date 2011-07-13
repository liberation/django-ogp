from django import template

register = template.Library()

@register.simple_tag
def ogp_namespace():
    """
    Returns the OGP namespace to put in the <html> tag.
    """
    return 'xmlns:og="http://ogp.me/ns#"'

@register.inclusion_tag('ogp.html')
def render_ogp(item):
    """
    Returns a dictionary containing a dictionary of OGP infos to be able to
    cycle through them in the template.
    """
    if not getattr(item, 'ogp_enabled', False):  # fail fast
        return {}
    ogp_infos = {}
    for method in dir(item):
        if method.startswith('ogp_') and method!='ogp_enabled':
            ogp_infos[method[4:].replace('_', ':')] = getattr(item, method)
    return {'ogp_infos': ogp_infos}
