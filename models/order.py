from models import db
from datetime import datetime
import pytz

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracking_number = db.Column(db.String(50), unique=True, nullable=False)
    sender_name = db.Column(db.String(100), nullable=False)
    sender_phone = db.Column(db.String(15), nullable=True)
    receiver_name = db.Column(db.String(100), nullable=False)
    receiver_phone = db.Column(db.String(15), nullable=True)
    receiver_address = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    declared_value = db.Column(db.Float, nullable=False)
    shipping_fee = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default="Chờ vận chuyển")
    create_time = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")))
    work_receiver = db.Column(db.String(50), nullable=True)
    def __repr__(self):
        return f"<Order {self.tracking_number} - {self.status}>"
