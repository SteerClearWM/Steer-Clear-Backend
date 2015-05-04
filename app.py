from flask import Flask
app = Flask(__name__)

@app.route('/')
def heartbeat():
	return "pulse"

if __name__ == "__main__":
	app.run()
