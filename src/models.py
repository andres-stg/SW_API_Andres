from flask_sqlalchemy import SQLAlchemy

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_year = db.Column(db.String(10), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'birth_year': self.birth_year
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    population = db.Column(db.String(20), nullable=False)
    terrain = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'population': self.population,
            'terrain': self.terrain
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    user = db.relationship('User', back_populates='favorites')
    planet = db.relationship('Planet')
    people = db.relationship('People')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id,
            'people_id': self.people_id
        }

User.favorites = db.relationship('Favorite', back_populates='user')


