from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models import db
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['work_place'] = user.workplace
            session['full_name'] = user.full_name
            session['role'] = user.role
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('main.index')) 
        else:
            flash('Sai tên đăng nhập hoặc mật khẩu!', 'danger')
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        cccd = request.form.get('cccd')
        address = request.form.get('address')
        role = request.form.get('role')
        workplace = request.form.get('workplace')
        
        if password != confirm_password:
            flash('Mật khẩu và xác nhận mật khẩu không khớp!', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác!', 'danger')
            return redirect(url_for('auth.register'))
        
        password_hash = generate_password_hash(password)
        new_user = User(
            username=username,
            password_hash=password_hash,
            full_name=full_name,
            phone=phone,
            cccd=cccd,
            address=address,
            role=role, 
            workplace=workplace
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Bạn đã đăng xuất!', 'info')
    return redirect(url_for('auth.login'))
