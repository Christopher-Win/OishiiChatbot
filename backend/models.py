from config import db

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
