from app import app

@app.route('/')
def heartbeat():
        return "pulse"
