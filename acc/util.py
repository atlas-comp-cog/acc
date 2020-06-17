import json
import math
import itertools

from clldutils import svg
from sqlalchemy.orm import joinedload

from clld.db.meta import DBSession
from clld.db.models import common

from acc.models import Species


def species_node(s, req):
    nex = sum(len(vs.values) for vs in s.valuesets)
    return {
        'name': s.name,
        'id': s.id,
        'bubble_size': math.log(5 * nex) * 10,
        'bubble': svg.data_url(svg.icon('cf60', 0.5)),
        'gbif_logo': req.static_url('acc:static/gbif.png'),
        'gbif_url': s.gbif_url,
        'gbif_name': s.gbif_name,
    }


def language_index_html(ctx=None, req=None, **kw):
    tree = []
    species = DBSession.query(Species).order_by(
        Species.kingdom, Species.phylum, Species.klass, Species.order, Species.family, Species.genus
    )
    for kingdom, items1 in itertools.groupby(species, lambda s: s.kingdom):
        n1 = {'name': 'Kingdom: ' + kingdom, 'children': []}
        for phylum, items2 in itertools.groupby(items1, lambda s: s.phylum):
            n2 = {'name': 'Phylum: ' + phylum, 'children': []}
            for klass, items3 in itertools.groupby(items2, lambda s: s.klass):
                n3 = {'name': 'Class: ' + klass, 'children': []}
                for order, items4 in itertools.groupby(items3, lambda s: s.order):
                    n4 = {'name': 'Order: ' + order, 'children': []}
                    for family, items5 in itertools.groupby(items4, lambda s: s.family):
                        n5 = {'name': 'Family: ' + family, 'children': []}
                        for genus, items6 in itertools.groupby(items5, lambda s: s.genus):
                            n5['children'].append({
                                'name': 'Genus: ' + genus,
                                'children': [species_node(s, req) for s in items6]})
                        n4['children'].append(n5)
                    n3['children'].append(n4)
                n2['children'].append(n3)
            n1['children'].append(n2)
        tree.append(n1)
    return dict(tree=json.dumps(tree))


def parameter_index_html(ctx=None, req=None, **kw):
    res = []
    for p in DBSession.query(common.Parameter).options(
        joinedload(common.Parameter.valuesets).joinedload(common.ValueSet.values)
    ):
        res.append((
            p,
            len(set(vs.language for vs in p.valuesets)),
            sum(len(vs.values) for vs in p.valuesets),
        ))
    return {'counts': res}
