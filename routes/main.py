from flask import Blueprint, render_template, session, redirect, url_for, flash

main_bp = Blueprint('main', __name__)

@main_bp.route('/index')
def index():
    if not session.get('username'):
        flash('Vui lòng đăng nhập trước!', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('index.html')
