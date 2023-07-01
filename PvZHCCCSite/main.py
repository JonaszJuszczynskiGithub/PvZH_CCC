from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    file = open(r'./PvZHCCC.py', 'r').read()
    return exec(file)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)
