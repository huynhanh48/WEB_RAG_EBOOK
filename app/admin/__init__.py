from flask import Blueprint

admin = Blueprint('admin', __name__)

# Import views ở cuối để tránh lỗi vòng lặp
from . import views
