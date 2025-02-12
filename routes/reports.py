from flask import Blueprint, jsonify, request, render_template, session, send_file
from models import db
from models.warehouse import Warehouse
from datetime import datetime
import pytz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab import pdfbase
from reportlab.pdfbase import pdfmetrics
import os

report_bp = Blueprint('report', __name__)

def register_fonts():
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont('DejaVu', font_path))
def create_pdf_report(data, report_type, date):
    register_fonts()
    
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    file_name = f"reports/BaoCao_{'XuatKho' if report_type == 'export' else 'NhapKho'}_{date}.pdf"
    
    c = canvas.Canvas(file_name, pagesize=letter)
    c.setFont("DejaVu", 16)
    
    title = f"Báo cáo {'Xuất' if report_type == 'export' else 'Nhập'} kho ngày {date}"
    c.drawString(100, 750, title)
    
    c.setFont("DejaVu", 12)
    headers = ["STT", "Mã vận đơn", "Người giao", "Thời gian", "Nơi làm việc", "Trạng thái"]
    x_positions = [50, 100, 200, 300, 400, 500]
    y_position = 700
    
    for i, header in enumerate(headers):
        c.drawString(x_positions[i], y_position, header)
    
    y_position -= 20
    for idx, item in enumerate(data, 1):
        c.drawString(x_positions[0], y_position, str(idx))
        c.drawString(x_positions[1], y_position, item.tracking_number)
        c.drawString(x_positions[2], y_position, item.shipper or "")
        time_str = item.export_time.strftime("%H:%M %d/%m/%Y") if report_type == 'export' else item.create_time.strftime("%H:%M %d/%m/%Y")
        c.drawString(x_positions[3], y_position, time_str)
        c.drawString(x_positions[4], y_position, item.workplace or "")
        c.drawString(x_positions[5], y_position, item.status or "")
        y_position -= 20
        
        if y_position < 50:
            c.showPage()
            c.setFont("DejaVu", 12)
            y_position = 700
    
    c.save()
    return file_name

@report_bp.route('/report', methods=['GET'])
def get_ware_house():
    return render_template('reports.html')

@report_bp.route('/report/export', methods=['GET'])
def export_report():
    date = request.args.get("date")
    if not date:
        return jsonify({"error": "Vui lòng cung cấp ngày"}), 400
    
    try:
        search_date = datetime.strptime(date, "%Y-%m-%d")
        vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        search_date = vietnam_tz.localize(search_date)
        
        warehouse_data = Warehouse.query.filter(
            db.func.date(Warehouse.export_time) == search_date.date()
        ).all()
        
        if not warehouse_data:
            return jsonify({"error": "Không có dữ liệu cho ngày này"}), 404
            
        file_path = create_pdf_report(warehouse_data, 'export', date)
        
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/report/import', methods=['GET'])
def import_report():
    date = request.args.get("date")
    if not date:
        return jsonify({"error": "Vui lòng cung cấp ngày"}), 400
    
    try:
        search_date = datetime.strptime(date, "%Y-%m-%d")
        vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        search_date = vietnam_tz.localize(search_date)
        
        warehouse_data = Warehouse.query.filter(
            db.func.date(Warehouse.create_time) == search_date.date()
        ).all()
        
        if not warehouse_data:
            return jsonify({"error": "Không có dữ liệu cho ngày này"}), 404
            
        file_path = create_pdf_report(warehouse_data, 'import', date)
        
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
