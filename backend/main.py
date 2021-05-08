from flask import Flask,render_template
from flask_restful import Resource, Api

app = Flask(__name__)

@app.route('')
def inicio():
    return 'conectado'

if __name__ == '__main__':
    app.run()