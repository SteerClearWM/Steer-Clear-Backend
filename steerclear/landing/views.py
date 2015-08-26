from flask import (
    Blueprint,
    render_template
)

landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/landing', methods=['GET'])
def land():
    # GET request. return landing page
    return render_template('landing.html')
