from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Movie(db.Model, SerializerMixin):
    __tablename__='movie_table'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    rating = db.Column(db.Integer)
    description = db.Column(db.String)
    image = db.Column(db.String)

    # Add relationship
    credit = db.relationship('Credit', back_populates='movie') 

    # Add serialization rules
    serialize_rules = ('-credit_table.movie', )



class Actor(db.Model, SerializerMixin):
    __tablename__='actor_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String)

    # Add relationship
    credit = db.relationship('Credit', back_populates='actor') 

    # Add serialization rules
    serialize_rules = ('-credit_table.actor', )

    # Add validation
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError("Scientist must have a name")
        return name
    @validates('age')
    def validate_age(self, key, value):
        if 10 < value:
            return value
        else:
            raise ValueError("Actor must be older than 10")



class Credit(db.Model, SerializerMixin):
    __tablename__='credit_table'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie_table.id"))
    actor_id = db.Column(db.Integer, db.ForeignKey("actor_table.id"))

    # Add relationship
    movie = db.relationship('Movie', back_populates='credit') 
    actor = db.relationship('Actor', back_populates='credit') 

    # Add serialization rules
    serialize_rules = ('-movie.credit_table', '-actor.credit_table')

    #Add validation
    @validates('role')
    def validate_role(self, key, value):
        roles = ["Performer", "Director", "Producor", "Playwright", "Lighting Design", "Sound Design", "Set Design"]
        if value in roles:
            return value
        else:
            raise ValueError("Not a valid role")
