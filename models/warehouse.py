from models import db
from datetime import datetime
import pytz

class Warehouse(db.Model):
    __tablename__ = 'warehouse'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracking_number = db.Column(db.String(50), nullable=False)
    shipper = db.Column(db.String(50), nullable=True)
    create_time = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")))
    export_time = db.Column(db.DateTime, nullable=True)
    workplace = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(50), nullable=True, default="Sẵn sàng")
