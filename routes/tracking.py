import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.order import Order
from models import db
from sqlalchemy import or_

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/manager-product', methods=['GET'])
def create_order_form():
    return render_template('manager_order.html')

@tracking_bp.route('/danhsachorder', methods=['GET'])
def get_all_order():
    if request.method == 'GET':
        sender_phone = request.args.get('sender_phone', '')
        receiver_phone = request.args.get('receiver_phone', '')

        query = Order.query

        if sender_phone:
            query = query.filter(Order.sender_phone.like(f'%{sender_phone}%'))
        if receiver_phone:
            query = query.filter(Order.receiver_phone.like(f'%{receiver_phone}%'))

        orders = query.all()

        orders_json = [
            {
                "id": order.id,
                "tracking_number": order.tracking_number,
                "sender_name": order.sender_name,
                "sender_phone": order.sender_phone,
                "receiver_name": order.receiver_name,
                "receiver_phone": order.receiver_phone,
                "status": order.status,
                "shipping_fee": order.shipping_fee
            }
            for order in orders
        ]
        return jsonify(orders_json)
    return jsonify({"error": "Phương thức không hợp lệ"}), 405

@tracking_bp.route('/search-orders', methods=['GET'])
def search_orders():
    sender_phone = request.args.get('sender_phone', '')
    receiver_phone = request.args.get('receiver_phone', '')

    query = Order.query

    conditions = []
    if sender_phone:
        conditions.append(Order.sender_phone.like(f'%{sender_phone}%'))
    if receiver_phone:
        conditions.append(Order.receiver_phone.like(f'%{receiver_phone}%'))

    if conditions:
        query = query.filter(or_(*conditions))

    orders = query.all()

    orders_json = [
        {
            "id": order.id,
            "tracking_number": order.tracking_number,
            "sender_name": order.sender_name,
            "sender_phone": order.sender_phone,
            "receiver_name": order.receiver_name,
            "receiver_phone": order.receiver_phone,
            "status": order.status,
            "shipping_fee": order.shipping_fee
        }
        for order in orders
    ]
    
    return jsonify(orders_json)

@tracking_bp.route('/capnhatorder', methods=['GET'])
def update_order():
    order_id = request.args.get('id')
    new_status = request.args.get('status')
    
    if not order_id or not new_status:
        flash("Thiếu tham số cập nhật!", "danger")
        return redirect(url_for('order.get_all_order'))
    
    order = Order.query.get(order_id)
    if order:
        order.status = new_status
        db.session.commit()
        flash("Cập nhật đơn hàng thành công!", "success")
    else:
        flash("Không tìm thấy đơn hàng!", "danger")
    
    return redirect(url_for('order.get_all_order'))