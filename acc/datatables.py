from clld.db.models.common import Language, Parameter, ValueSet
from clld.db.util import get_distinct_values
from clld.web.datatables.base import LinkCol, RefsCol, Col, DetailsRowLinkCol, LinkToMapCol
from clld.web.datatables.value import Values, ValueNameCol
from clld.web.datatables.language import Languages
from clld.web.util.htmllib import HTML

from acc import models


class GBIFLinkCol(Col):
    def format(self, item):
        if not item.gbif_url:
            return ''
        return HTML.a(
            HTML.img(width='20', src=self.dt.req.static_url('acc:static/gbif.png')),
            item.gbif_name,
            href=item.gbif_url)


class SpeciesTable(Languages):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            Col(self, 'experiments', model_col=models.Species.count_experiments, input_size='mini'),
            GBIFLinkCol(self, 'gbif', sTitle='GBIF', model_col=models.Species.gbif_name),
            Col(self, 'class', model_col=models.Species.klass, choices=get_distinct_values(models.Species.klass)),
            Col(self, 'order', model_col=models.Species.order, choices=get_distinct_values(models.Species.order)),
            Col(self, 'family', model_col=models.Species.family, choices=get_distinct_values(models.Species.family)),
            Col(self, 'genus', model_col=models.Species.genus, choices=get_distinct_values(models.Species.genus)),
        ]


class Experiments(Values):
    def base_query(self, query):
        query = Values.base_query(self, query)
        if not self.language and not self.parameter:
            query = query.join(ValueSet.language).join(ValueSet.parameter)
        return query

    def col_defs(self):
        type_col = Col(
            self,
            'type',
            model_col=models.Experiment.type,
            choices=get_distinct_values(models.Experiment.type))
        if self.parameter:
            return [
                ValueNameCol(self, 'value'),
                LinkCol(
                    self,
                    'language',
                    model_col=Language.name,
                    get_object=lambda i: i.valueset.language),
                Col(self, 'sample_size', model_col=models.Experiment.sample_size),
                type_col,
                RefsCol(self, 'source'),
                DetailsRowLinkCol(self, '#', button_text='abstract'),
            ]
        if self.language:
            return [
                ValueNameCol(self, 'value'),
                Col(self, 'sample_size', model_col=models.Experiment.sample_size),
                type_col,
                LinkCol(
                    self,
                    'parameter',
                    model_col=Parameter.name,
                    get_object=lambda i: i.valueset.parameter),
                RefsCol(self, 'source'),
                DetailsRowLinkCol(self, '#', button_text='abstract'),
            ]
        return [
            ValueNameCol(self, 'value'),
            LinkCol(
                self,
                'language',
                model_col=Language.name,
                get_object=lambda i: i.valueset.language),
            Col(self, 'sample_size', model_col=models.Experiment.sample_size),
            type_col,
            LinkCol(
                self,
                'parameter',
                model_col=Parameter.name,
                get_object=lambda i: i.valueset.parameter),
            RefsCol(self, 'source'),
            DetailsRowLinkCol(self, '#', button_text='abstract'),
        ]


def includeme(config):
    config.register_datatable('languages', SpeciesTable)
    config.register_datatable('values', Experiments)
