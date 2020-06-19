from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import common, HasSourceNotNullMixin


@implementer(interfaces.ILanguage)
class Species(CustomModelMixin, common.Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    gbif_name = Column(Unicode)
    gbif_url = Column(Unicode)
    kingdom = Column(Unicode)
    phylum = Column(Unicode)
    klass = Column(Unicode)
    order = Column(Unicode)
    family = Column(Unicode)
    genus = Column(Unicode)
    count_experiments = Column(Integer)


@implementer(interfaces.IParameter)
class Ability(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    domain_name = Column(Unicode)
    area = Column(Unicode)


@implementer(interfaces.IContribution)
class Review(CustomModelMixin, common.Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)


class ExperimentReference(Base, HasSourceNotNullMixin):

    """References for a set of values (related to one parameter and one language).

    These references can be interpreted as justifications why a language does not "have"
    certain values for a parameter, too.
    """

    __table_args__ = (UniqueConstraint('value_pk', 'source_pk', 'description'),)

    value_pk = Column(Integer, ForeignKey('value.pk'), nullable=False)
    value = relationship(common.Value, innerjoin=True, backref="references")


@implementer(interfaces.IValue)
class Experiment(CustomModelMixin, common.Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    type = Column(Unicode)
    sample_size = Column(Unicode)
