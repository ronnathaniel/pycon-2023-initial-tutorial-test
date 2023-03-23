
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World! from our plain Flask App\n'


@app.route('/error')
def error():
    1 / 0


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

