# -*- coding: utf-8 -*-
from flask import Flask

# Create small app
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello I`m index' 

@app.route('/ajax')
def ajax():
    pass

@app.route('/dcu', methods=['POST'])
def dcu():
    pass


# Self server mode
if __name__ == '__main__':
    app.run()
