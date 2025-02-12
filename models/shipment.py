from models import db

class Shipment(db.Model):
    __tablename__ = 'shipments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    route = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="Đang vận chuyển")

    def __repr__(self):
        return f"<Shipment Order: {self.order_id} - {self.status}>"
