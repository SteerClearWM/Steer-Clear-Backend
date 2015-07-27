from flask import Blueprint, render_template
from flask.ext.login import login_required

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
#@login_required
def index():
    return render_template('index.html')
