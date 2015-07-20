from flask import Blueprint, render_template

driver_portal_bp = Blueprint('driver_portal', __name__)

"""
heartbeat
---------
Simple check to see if server is running
"""
@driver_portal_bp.route('/')
def heartbeat():
        return "pulse"

@driver_portal_bp.route('/index')
def index():
    return render_template('index.html')
