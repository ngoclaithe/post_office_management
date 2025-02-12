import uuid
from flask import Blueprint, render_template, request, jsonify, session
from models.order import Order
from models import db
from models.user import User
from models.order_shipper import OrderShipper

shipping_bp = Blueprint('shipping', __name__)

@shipping_bp.route('/manager-ship', methods=['GET'])
def get_manager_ship():
    return render_template('manage_shipping.html')
@shipping_bp.route('/my_shipper', methods=['GET'])
def get_my_shipper():
    return render_template('my_order.html')
@shipping_bp.route('/laydonhangphancong', methods=['GET'])
def lay_don_hang_phan_cong():
    shipper_id = request.args.get("shipper_id")

    if not shipper_id:
        return jsonify({"message": "Thiếu thông tin shipper_id"}), 400

    order_shippers = OrderShipper.query.filter_by(shipper_id=shipper_id).all()

    if not order_shippers:
        return jsonify({"message": "Không có đơn hàng nào được phân công cho nhân viên giao hàng này"}), 404

    orders_details = []
    for order_shipper in order_shippers:
        order = Order.query.filter_by(tracking_number=order_shipper.tracking_number).first()
        if order:
            order_details = {
                "ma_van_don": order.tracking_number,
                "dia_chi_nhan": order.receiver_address,
                "so_dien_thoai": order.receiver_phone,
                "ten_nguoi_nhan": order.receiver_name,
            }
            orders_details.append(order_details)

    return jsonify(orders_details)
    

@shipping_bp.route('/laydanhsachhanghoa', methods=['GET'])
def lay_danh_sach_hang_hoa():
    work_place = request.args.get('work_place')
    orders = Order.query.filter_by(status='Chờ vận chuyển', work_receiver=work_place).all()
    
    result = [
        {
            "ma_van_don": order.tracking_number,  
            "dia_chi_nhan": order.receiver_address,  
            "so_dien_thoai": order.receiver_phone  
        } 
        for order in orders
    ]
    
    return jsonify(result)

@shipping_bp.route('/laydanhsachgiaohang', methods=['GET'])
def lay_danh_sach_shipper():
    work_place = request.args.get('work_place')
    shippers = User.query.filter_by(role='shipper', workplace=work_place).all()
    
    result = [
        {   
            "id_shipper": shipper.id,
            "full_name": shipper.full_name, 
            "phone": shipper.phone  
        }
        for shipper in shippers
    ]
    
    return jsonify(result)
@shipping_bp.route('/quanlyvandon', methods=['POST'])
def dieu_phoi_don_hang():
    data = request.get_json()
    ma_van_don = data.get('ma_van_don')
    id_shipper = data.get('id_shipper')
    id_post_office = data.get('id_post_office')

    if not ma_van_don:
        return jsonify({"message": "Thiếu thông tin mã vận đơn"}), 400

    order = Order.query.filter_by(tracking_number=ma_van_don).first()
    if not order:
        return jsonify({"message": "Đơn hàng không tồn tại"}), 404

    if id_shipper:
        shipper = User.query.get(id_shipper)
        if not shipper:
            return jsonify({"message": "Nhân viên giao hàng không tồn tại"}), 404
        order.status = f"{shipper.full_name} đang giao hàng"
        new_order_shipper = OrderShipper(
            tracking_number=ma_van_don,
            shipper_id=id_shipper
        )
        db.session.add(new_order_shipper)
    elif id_post_office:
        order.status = f"Đang chuyến sang bưu cục {id_post_office}"
    else:
        return jsonify({"message": "Thiếu thông tin giao hàng (id_shipper hoặc id_post_office)"}), 400

    db.session.commit()
    return jsonify({"message": "Cập nhật đơn hàng thành công"})

