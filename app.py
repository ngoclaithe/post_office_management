
from flask import Flask
from models import db, init_db
from routes.auth import auth_bp
from routes.main import main_bp
from routes.order import order_bp
from routes.tracking import tracking_bp
from routes.shipping import shipping_bp
from routes.warehouse import warehouse_bp
from routes.reports import report_bp
from config import Config  

app = Flask(__name__)
app.config.from_object(Config)  

init_db(app)
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(order_bp)
app.register_blueprint(tracking_bp)
app.register_blueprint(shipping_bp)
app.register_blueprint(warehouse_bp)
app.register_blueprint(report_bp)
if __name__ == "__main__":
    app.run(debug=True)
