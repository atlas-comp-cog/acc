from pyramid.config import Configurator

from clld.interfaces import IValue, ILinkAttrs

# we must make sure custom models are known at database initialization!
from acc import models

_ = lambda s: s
_('Language')
_('Languages')
_('Contribution')
_('Contributions')
_('Contributor')
_('Contributors')
_('Parameter')
_('Parameters')
_('Value')
_('Values')
_('ValueSet')
_('ValueSets')


def link_attrs(req, obj, **kw):
    if IValue.providedBy(obj):
        kw['href'] = req.route_url('valueset', id=obj.valueset.id, **kw.pop('url_kw', {}))

    return kw


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.registry.registerUtility(link_attrs, ILinkAttrs)
    return config.make_wsgi_app()
