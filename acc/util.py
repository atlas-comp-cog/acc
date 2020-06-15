from sqlalchemy.orm import joinedload

from clld.db.meta import DBSession
from clld.db.models import common


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
