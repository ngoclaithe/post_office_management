import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.order import Order
from models import db

order_bp = Blueprint('order', __name__)

@order_bp.route('/taodon', methods=['GET'])
def create_order_form():
    return render_template('create_order.html')

@order_bp.route('/nhanvientaoorder', methods=['POST'])
def create_order():
    if request.method == 'POST':
        sender_name      = request.form.get('sender_name')
        sender_phone     = request.form.get('sender_phone')
        receiver_name    = request.form.get('receiver_name')
        receiver_phone   = request.form.get('receiver_phone')
        receiver_address = request.form.get('receiver_address')
        weight           = request.form.get('weight')
        declared_value   = request.form.get('declared_value')
        shipping_fee     = request.form.get('shipping_fee')
        note             = request.form.get('note')
        work_receiver    = request.form.get('work_receiver')
        
        if not all([sender_name, receiver_name, receiver_address, weight, declared_value, shipping_fee]):
            return jsonify({
                "success": False,
                "message": "Vui lòng nhập đầy đủ thông tin bắt buộc!"
            }), 400
        
        try:
            weight = float(weight)
            declared_value = float(declared_value)
            shipping_fee = float(shipping_fee)  
        except ValueError:
            return jsonify({
                "success": False,
                "message": "Trọng lượng, giá trị khai báo và phí vận chuyển phải là số!"
            }), 400
        
        tracking_number = str(uuid.uuid4())[:8].upper()
        
        new_order = Order(
            tracking_number   = tracking_number,
            sender_name       = sender_name,
            sender_phone      = sender_phone,
            receiver_name     = receiver_name,
            receiver_phone    = receiver_phone,
            receiver_address  = receiver_address,
            weight            = weight,
            declared_value    = declared_value,
            shipping_fee      = shipping_fee,
            note              = note,
            status            = "Chờ vận chuyển",
            work_receiver     = work_receiver,
        )
        
        try:
            db.session.add(new_order)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": "Lỗi khi tạo đơn hàng."
            }), 500
        
        return jsonify({
            "success": True,
            "message": f"Tạo đơn hàng thành công với mã vận đơn: {tracking_number}"
        })
    else:
        return jsonify({
            "success": False,
            "message": "Phương thức không hợp lệ!"
        }), 405
