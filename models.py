from config import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    hero_powers = db.relationship(
        'HeroPower',
        back_populates='hero',
        cascade='all, delete'
    )

    serialize_rules = ('-hero_powers.hero',)


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    hero_powers = db.relationship(
        'HeroPower',
        back_populates='power',
        cascade='all, delete'
    )

    serialize_rules = ('-hero_powers.power',)

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("validation errors")
        return description


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("validation errors")
        return strength
