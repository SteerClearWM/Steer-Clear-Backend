from steerclear import app
from flask import render_template

"""
heartbeat
---------
Simple check to see if server is running
"""
@app.route('/')
def heartbeat():
        return "pulse"

@app.route('/index')
def index():
    return render_template('index.html')
