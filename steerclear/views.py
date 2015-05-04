from steerclear import app

@app.route('/')
def heartbeat():
        return "pulse"
