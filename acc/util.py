import json
import math
import itertools

from clldutils import svg
from sqlalchemy.orm import joinedload
import newick

from clld.db.meta import DBSession
from clld.db.models import common

from acc.models import Species


def species_node(s, req):
    nex = sum(len(vs.values) for vs in s.valuesets)
    return {
        'name': s.name,
        'id': s.id,
        'experiments': nex,
        'bubble_size': math.log(5 * nex) * 10,
        'bubble': svg.data_url(svg.icon('cf60', 0.5)),
        'gbif_logo': req.static_url('acc:static/gbif.png'),
        'gbif_url': s.gbif_url,
        'gbif_name': s.gbif_name,
    }


def language_index_html(ctx=None, req=None, **kw):
    node_data = {}
    tree = []
    ntrees = []
    species = DBSession.query(Species).order_by(
        Species.kingdom, Species.phylum, Species.klass, Species.order, Species.family, Species.genus
    )
    for kingdom, items1 in itertools.groupby(species, lambda s: s.kingdom):
        n1 = {'name': 'Kingdom: ' + kingdom, 'children': []}
        node1 = newick.Node()
        for phylum, items2 in itertools.groupby(items1, lambda s: s.phylum):
            n2 = {'name': 'Phylum: ' + phylum, 'children': []}
            node2 = newick.Node()
            for klass, items3 in itertools.groupby(items2, lambda s: s.klass):
                n3 = {'name': 'Class: ' + klass, 'children': []}
                node3 = newick.Node()
                for order, items4 in itertools.groupby(items3, lambda s: s.order):
                    n4 = {'name': 'Order: ' + order, 'children': []}
                    node4 = newick.Node()
                    for family, items5 in itertools.groupby(items4, lambda s: s.family):
                        n5 = {'name': 'Family: ' + family, 'children': []}
                        node5 = newick.Node()
                        for genus, items6 in itertools.groupby(items5, lambda s: s.genus):
                            items6 = list(items6)
                            node6 = newick.Node.create(descendants=[
                                newick.Node('%s{__id__%s}' % (s.name.replace(' ', '_'), s.id)) for s in items6
                            ])
                            node_data.update({s.id: species_node(s, req) for s in items6})
                            n5['children'].append({
                                'name': 'Genus: ' + genus,
                                'children': [species_node(s, req) for s in items6]})
                            node5.add_descendant(node6)
                        n4['children'].append(n5)
                        node4.add_descendant(node5)
                    n3['children'].append(n4)
                    node3.add_descendant(node4)
                n2['children'].append(n3)
                node2.add_descendant(node3)
            n1['children'].append(n2)
            node1.add_descendant(node2)
        ntrees.append(node1)
        tree.append(n1)
    return dict(tree=json.dumps(tree), newick=newick.dumps(ntrees), node_data=json.dumps(node_data))


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
