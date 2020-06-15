from clld.db.models.common import Language, Parameter, ValueSet
from clld.db.util import get_distinct_values
from clld.web.datatables.base import LinkCol, RefsCol, Col, DetailsRowLinkCol
from clld.web.datatables.value import Values, ValueNameCol

from acc import models


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
    config.register_datatable('values', Experiments)
