from flask import render_template
from . import admin  # Đảm bảo import từ module hiện tại

@admin.route('/')
def dashboard():
    return render_template('admin/dashboard.html')
