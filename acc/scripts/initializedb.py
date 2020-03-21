import sys

from clld.scripts.util import initializedb, Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import EntryType

import acc
from acc import models


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
                name=ex.contribution_name,
                description=str(ex.source),
                source=src,
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
            )
        species = data['Species'].get(ex.species_id)
        if not species:
            species = data.add(
                models.Species,
                ex.species_id,
                id=ex.species_id,
                name=ex.species,
                description=ex.species_latin,
            )
        vs = data.add(
            models.Experiment,
            ex.id,
            id=ex.id,
            language=species,
            contribution=contrib,
            parameter=param,
        )
        DBSession.add(common.Value(
            id=ex.id,
            valueset=vs,
            name=ex.sample_size,
        ))
    for sid, lat, lon in [
        ('gorillagorilla', 85, 170),
        ('lemurcatta', -70, 170),
    ]:
        data['Species'][sid].longitude = lon
        data['Species'][sid].latitude = lat


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)