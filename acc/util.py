import json
import math
import itertools
import collections
from xml.etree import ElementTree as et

from clldutils import color
from clldutils import svg
from sqlalchemy.orm import joinedload
import newick

from clld.db.meta import DBSession
from clld.db.models import common
from clld.web.util.component import Component
from clld.web.util.helpers import JS

from acc.models import Species


class Tree(Component):
    __template__ = 'tree.mako'

    def __init__(self, data):
        self.data = data


def iter_pie_paths(*chunks):
    xml = et.fromstring(svg.pie(chunks, ('#000', '#fff'), width=12))
    for path in xml.findall('.//{http://www.w3.org/2000/svg}path'):
        res = {k: v for k, v in path.attrib.items()}
        res['style'] = res['style'].replace('none', '#000')
        res['transform'] += ' translate(-6 6)'
        yield res


def species_node(s, req, nex):
    return {
        'name': s.name,
        'id': s.id,
        'experiments': nex,
        'bubble_size': math.log(5 * nex) * 10,
        'bubble': svg.data_url(svg.icon('cf60', 0.5)),
        'gbif_logo': req.static_url('acc:static/gbif.png'),
        'gbif_url': s.gbif_url,
        'gbif_name': s.gbif_name,
        'family': s.family,
    }


def coverage_data(req, nid, rank, subranks, coverage):
    _, total = req.dataset.jsondata['gbif_coverage'][nid]
    d = coverage
    for comp in nid.split('_'):
        d = d[comp]
    in_ = len(d) if isinstance(d, dict) else d
    return dict(
        tooltip='<p><strong>{} {}</strong><br/>{} of {} {}</p>'.format(
            rank, nid.split('_')[-1], in_, total, subranks),
        paths=list(iter_pie_paths(in_, total - in_))
    )


def tree_data(req, species_query, experiment_count=lambda s: s.count_experiments):
    node_data = {}
    ntrees = []
    colormap = collections.Counter()
    colormap2 = collections.Counter()
    count_leafs = species_query.count()
    species = species_query.order_by(
        Species.kingdom, Species.phylum, Species.klass, Species.order, Species.family, Species.genus
    ).options(joinedload(common.Language.valuesets).joinedload(common.ValueSet.values))
    coverage = {}
    nodes = []

    for kingdom, items1 in itertools.groupby(species, lambda s: s.kingdom):
        node1 = newick.Node()
        for phylum, items2 in itertools.groupby(items1, lambda s: s.phylum):
            nid = '_'.join((phylum,))
            nodes.append((nid, 'Phylum', 'classes'))
            if phylum not in coverage:
                coverage[phylum] = {}
            #node_data[nid] = coverage_data(req, nid, 'Phylum', 'classes')

            node2 = newick.Node(nid)
            for klass, items3 in itertools.groupby(items2, lambda s: s.klass):
                nid = '_'.join((phylum, klass))
                nodes.append((nid, 'Class', 'orders'))
                if klass not in coverage[phylum]:
                    coverage[phylum][klass] = {}
                #node_data[nid] = coverage_data(req, nid, 'Class', 'orders')

                node3 = newick.Node(nid)
                for order, items4 in itertools.groupby(items3, lambda s: s.order):
                    nid = '_'.join((phylum, klass, order))
                    nodes.append((nid, 'Order', 'families'))
                    if order not in coverage[phylum][klass]:
                        coverage[phylum][klass][order] = {}
                    #node_data[nid] = coverage_data(req, nid, 'Order', 'families')

                    node4 = newick.Node(nid)
                    for family, items5 in itertools.groupby(items4, lambda s: s.family):
                        nid = '_'.join((phylum, klass, order, family))
                        nodes.append((nid, 'Family', 'genera'))
                        if family not in coverage[phylum][klass][order]:
                            coverage[phylum][klass][order][family] = {}
                        #node_data[nid] = coverage_data(req, nid, 'Family', 'genera')

                        node5 = newick.Node(nid)
                        for genus, items6 in itertools.groupby(items5, lambda s: s.genus):
                            nid = '_'.join((phylum, klass, order, family, genus))
                            nodes.append((nid, 'Genus', 'species'))
                            #node_data[nid] = coverage_data(req, nid, 'Genus', 'species')

                            items6 = list(items6)
                            coverage[phylum][klass][order][family][genus] = len(items6)

                            colormap.update([s.family for s in items6])
                            colormap2.update([s.klass for s in items6])
                            node6 = newick.Node.create(name=nid, descendants=[
                                newick.Node('%s{__id__%s}' % (s.name.replace(' ', '_'), s.id)) for s in items6
                            ])
                            node_data.update({s.id: species_node(s, req, experiment_count(s)) for s in items6})
                            node5.add_descendant(node6)
                        node4.add_descendant(node5)
                    node3.add_descendant(node4)
                node2.add_descendant(node3)
            node1.add_descendant(node2)
        ntrees.append(node1)

    node_data.update({
        nid: coverage_data(req, nid, rank, subranks, coverage)
        for nid, rank, subranks in nodes
    })

    res = dict(
        count_leafs=count_leafs,
        newick=newick.dumps(ntrees),
        colormap={
            k[0]: (v, svg.data_url(svg.icon(v.replace('#', 'c'))))
            for k, v in zip(colormap.most_common(), color.qualitative_colors(len(colormap)))},
        colormap2={
            k[0]: (v, svg.data_url(svg.icon(v.replace('#', 's'))))
            for k, v in zip(colormap2.most_common(), color.qualitative_colors(len(colormap), set='tol'))},
        node_data=node_data)
    res['edgecolors'] = {k: v[0] for k, v in res['colormap2'].items()}
    return res


def language_index_html(ctx=None, req=None, **kw):
    return dict(tree=Tree(tree_data(
        req,
        DBSession.query(Species),
    )))


def parameter_detail_html(context=None, req=None, **kw):
    return dict(tree=Tree(tree_data(
        req,
        DBSession.query(Species).join(common.ValueSet).join(common.Parameter)
        .filter(common.Parameter.pk == context.pk).distinct(),
        experiment_count=lambda s: sum(len(vs.values) for vs in s.valuesets if vs.parameter_pk == context.pk)
    )))


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
