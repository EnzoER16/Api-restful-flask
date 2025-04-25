from models.db import db

class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(15), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    number_plate = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, brand, model, number_plate):
        self.brand = brand
        self.model = model
        self.number_plate = number_plate

    def serialize(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'number_plate': self.number_plate
        }