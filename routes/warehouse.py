from flask import Blueprint, jsonify, request, render_template, session
from models import db
from models.warehouse import Warehouse
from models.user import User
from datetime import datetime
import pytz

warehouse_bp = Blueprint('warehouse', __name__)

class WarehouseStatus:
    READY = 'Sẵn sàng'
    IN_TRANSIT = 'Đang vận chuyển' 
    DEPARTED = 'Đã rời kho'
    PENDING = 'Chờ xử lý'
@warehouse_bp.route('/manager-warehouse', methods=['GET'])
def get_ware_house():
    return render_template('warehouse.html')
@warehouse_bp.route('/laydanhsachkhohang/<workplace>')
def lay_danh_sach_kho_hang(workplace):
    try:
        warehouses = db.session.query(Warehouse, User.full_name.label('shipper_name')).outerjoin(
            User, Warehouse.shipper == User.id
        ).filter(Warehouse.workplace == workplace).all()
        
        return jsonify([{
            'id': w.Warehouse.id,
            'tracking_number': w.Warehouse.tracking_number,
            'shipper': w.shipper_name,  
            'create_time': w.Warehouse.create_time.isoformat() if w.Warehouse.create_time else None,
            'workplace': w.Warehouse.workplace,
            'status': w.Warehouse.status
        } for w in warehouses])
    except Exception as e:
        print(f"Error: {str(e)}") 
        return jsonify({'error': str(e)}), 500

# @warehouse_bp.route('/laydanhsachgiaohang')
# def lay_danh_sach_giao_hang():
#     try:
#         workplace = request.args.get('work_place')
#         if not workplace:
#             return jsonify({'error': 'Thiếu thông tin workplace'}), 400
            
#         shippers = User.query.filter_by(
#             work_place=workplace,
#             role='shipper',
#             active=True
#         ).all()
        
#         return jsonify([{
#             'id': s.id,
#             'name': s.full_name
#         } for s in shippers])
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@warehouse_bp.route('/nhapkho', methods=['POST'])
def nhap_kho():
    try:
        data = request.get_json()
        tracking_number = data.get('tracking_number')
        workplace = data.get('workplace')

        if not tracking_number or not workplace:
            return jsonify({
                'success': False,
                'message': 'Thiếu thông tin tracking number hoặc workplace'
            }), 400

        existing = Warehouse.query.filter_by(tracking_number=tracking_number).first()
        if existing:
            return jsonify({
                'success': False,
                'message': 'Mã vận đơn đã tồn tại trong hệ thống'
            }), 400

        warehouse = Warehouse(
            tracking_number=tracking_number,
            workplace=workplace,
            status=WarehouseStatus.READY,
            create_time=datetime.now()
        )
        
        db.session.add(warehouse)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Nhập kho thành công'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi khi nhập kho: {str(e)}'
        }), 500
@warehouse_bp.route('/xuatkho', methods=['POST'])
def xuat_kho():
    try:
        data = request.get_json()
        warehouse_id = data.get('id')
        shipper_id = data.get('driver_id')
        print("Gia tri id ship", shipper_id)

        warehouse = Warehouse.query.get(warehouse_id)
        if not warehouse:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy đơn hàng trong kho'
            }), 404

        if warehouse.status != WarehouseStatus.READY:
            return jsonify({
                'success': False,
                'message': 'Đơn hàng không ở trạng thái sẵn sàng để xuất kho'
            }), 400

        shipper = User.query.get(shipper_id)
        if not shipper:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy tài xế'
            }), 404

        warehouse.shipper = shipper_id
        warehouse.status = WarehouseStatus.DEPARTED
        warehouse.export_time = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Xuất kho thành công'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Lỗi khi xuất kho: {str(e)}'
        }), 500
