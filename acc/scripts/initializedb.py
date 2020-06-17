from clld.scripts.util import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import EntryType

import acc
from acc import models

COORDS = [
    ('homosapiens', 84, 152),
    ('panpaniscus', 81.5, 152),
    ('pantroglodytes', 78, 152),
    ('gorillagorilla', 73, 152),
    ('pongoabelii', 67, 152),
    ('pongopygmaeus', 67, 152),
    ('pongospp', 67, 152),
    ('macacafascicularis', 47, 152),
    ('macacafuscata', 47, 152),
    ('macacamulatta', 47, 152),

    ('papiocynocephalusursinus', 11, 152),
    ('papiopapio', 10, 152),
    ('papioanubis', 9, 152),

    ('callithrixjacchus', -28, 152),
    ('saimirisciureussaimiriboliviensi', -44, 152),
    ('propithecusverreauxiverreauxi', -57, 152),
    ('lemurcatta', -67, 152),
    ('eulemurfulvusrufus', -67, 152),
    ('vareciavariegatavariegata', -67, 152),
]


def main(args):
    data = Data()

    dataset = common.Dataset(
        id=acc.__name__,
        name="Atlas of Comparative Cognition",
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        domain='acc.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})

    DBSession.add(dataset)

    for ex in args.api.experiments:
        src = data['Source'].get(ex.source.id)
        if not src:
            ex.source.genre = EntryType.get(ex.source.genre)
            src = data.add(common.Source, ex.source.id, _obj=bibtex2source(ex.source))
        contributor = data['Contributor'].get(ex.contributor_id)
        if not contributor:
            contributor = data.add(
                common.Contributor,
                ex.contributor_id,
                id=ex.contributor_id,
                name=str(ex.reviewer),
            )
        contrib = data['Review'].get(ex.contribution_id)
        if not contrib:
            contrib = data.add(
                models.Review,
                ex.contribution_id,
                id=ex.contribution_id,
                name=ex.review_title,
            )
        ccid = (ex.contribution_id, ex.contributor_id)
        if ccid not in data['ContributionContributor']:
            data.add(
                common.ContributionContributor,
                ccid,
                contribution=contrib,
                contributor=contributor)
        param = data['Ability'].get(ex.parameter_id)
        if not param:
            param = data.add(
                models.Ability,
                ex.parameter_id,
                id=ex.parameter_id,
                name=ex.parameter,
                domain_name=ex.domain,
                area=ex.area,
            )
        species = data['Species'].get(ex.species_id)
        if not species:
            species = data.add(
                models.Species,
                ex.species_id,
                id=ex.species_id,
                name=ex.species,
                description=ex.species_latin,
                gbif_name=ex.gbif.name,
                gbif_url=ex.gbif.url,
                kingdom=ex.gbif.classification.kingdom,
                phylum=ex.gbif.classification.phylum,
                klass=ex.gbif.classification.klass,
                order=ex.gbif.classification.order,
                family=ex.gbif.classification.family,
                genus=ex.gbif.classification.genus,
            )
        vsid = (species.id, contrib.id, param.id)
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet,
                vsid,
                id='-'.join(vsid),
                language=species,
                contribution=contrib,
                parameter=param,
            )
        v = data.add(
            models.Experiment,
            ex.id,
            id=ex.id,
            valueset=vs,
            sample_size=ex.sample_size,
            type=ex.type,
            description=ex.source_abstract,
        )
        DBSession.add(models.ExperimentReference(source=src, value=v))
    for sid, lat, lon in COORDS:
        data['Species'][sid].longitude = lon
        data['Species'][sid].latitude = lat


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
