from flask import Blueprint, render_template, redirect, url_for
from flask.ext.login import login_required, current_user

from steerclear.utils.permissions import admin_permission

driver_portal_bp = Blueprint('driver_portal', __name__)

"""
heartbeat
---------
Simple check to see if server is running
"""
@driver_portal_bp.route('/')
def heartbeat():
    return render_template('landing.html')

@driver_portal_bp.route('/index')
@login_required
@admin_permission.require(http_exception=403)
def index():
    return render_template('index.html')

@driver_portal_bp.route('/privacy-policy', defaults={'path': 'index.html'})
@driver_portal_bp.route('/privacy-policy/<path:path>')
def privacy_policy(path):
    return render_template('privacy-policy/' + path)
