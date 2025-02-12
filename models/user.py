from models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    cccd = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    workplace = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<User {self.username} - {self.role}>"
