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
from clld.db.models import common


@implementer(interfaces.ILanguage)
class Species(CustomModelMixin, common.Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)


@implementer(interfaces.IParameter)
class Ability(CustomModelMixin, common.Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)


@implementer(interfaces.IContribution)
class Review(CustomModelMixin, common.Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    source_pk = Column(Integer, ForeignKey('source.pk'))
    source = relationship(common.Source, backref='papers')


@implementer(interfaces.IValueSet)
class Experiment(CustomModelMixin, common.ValueSet):
    pk = Column(Integer, ForeignKey('valueset.pk'), primary_key=True)
    type = Column(Unicode)
    sample_size = Column(Unicode)
