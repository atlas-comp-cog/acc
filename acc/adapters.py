import math

from clld.interfaces import IParameter, ILanguage, IIndex
from clld.web.adapters.geojson import GeoJsonParameter, GeoJsonLanguages, GeoJson


class ACCGeoJsonLanguages(GeoJsonLanguages):
    def feature_properties(self, ctx, req, species):
        res = GeoJsonLanguages.feature_properties(self, ctx, req, species)
        nex = sum(len(vs.values) for vs in species.valuesets)
        res['icon_size'] = math.log(5 * nex) * 10
        res['label'] = '{}: {} experiments'.format(species.name, nex)
        return res


class ACCGeoJsonParameter(GeoJsonParameter):
    def feature_properties(self, ctx, req, valueset):
        res = GeoJsonParameter.feature_properties(self, ctx, req, valueset)
        res['icon_size'] = math.log(5 * len(valueset.values)) * 10
        res['label'] = '{}: {} experiments'.format(valueset.language.name, len(valueset.values))
        return res


def includeme(config):
    config.register_adapter(
        ACCGeoJsonLanguages,
        ILanguage,
        IIndex,
        name=GeoJson.mimetype)
    config.register_adapter(ACCGeoJsonParameter, IParameter)
