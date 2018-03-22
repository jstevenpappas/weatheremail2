"""
.. module:: models
   :synopsis: SQLAlchemy module containing classes that model the entities
        our application interacts with.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class Person(db.Model):
    """Person model.

    Notes:
        Self explaining class... but one thing worthy of mention is the
            ForeignKey ref Person.city_id to City.id.
        Also, the intentional length limit on the email attribute to 254
            according to the specs in RFC 3696.

    Attributes are defined below.
    """
    id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.DateTime(timezone=True),
                             server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    # RFC 3696 Errata states upper length of email addresses is 254 chars
    email = db.Column(db.String(254), index=True, unique=True, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    def __repr__(self):
        return '{email}'.format(email=self.email)


class City(db.Model):
    """City model.

    Attributes are defined below.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    persons = db.relationship('Person', backref='person', lazy=True)

    def __repr__(self):
        return '{name}, {state}'.format(name=self.name, state=self.state)
