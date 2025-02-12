from models import db
from datetime import datetime
import pytz

class OrderShipper(db.Model):
    __tablename__ = 'orders_shipper'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracking_number = db.Column(db.String(50), unique=True, nullable=False)
    shipper_id = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")))
    

