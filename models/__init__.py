from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        from models.user import User
        from models.order import Order
        from models.shipment import Shipment
        from models.warehouse import Warehouse
        from models.order_shipper import OrderShipper

        db.create_all()
        print("Database tables created successfully!")
