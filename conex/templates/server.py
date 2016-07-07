#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, emit
import eventlet

import dill as pickle

app = Flask(__name__)
app.debug = {{ debug|default(False) }}
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

{% for event, functions in subscriptions.items() %}
{% set outer_loop = loop %}
{% for func in functions %}
func_{{ outer_loop.index }}_{{loop.index}} = pickle.loads({{ func }})
{% endfor %}
{% endfor %}

{% for event, functions in subscriptions.items() %}
{% set outer_loop = loop %}
@socketio.on({{ event }})
def _(x):
    {% for func in functions %}
    foo = copy_current_request_context(func_{{ outer_loop.index }}_{{loop.index}})
    eventlet.spawn(foo, x)
    {% endfor %}
{% endfor %}

if __name__ == '__main__':
    socketio.run(app, host={{ host }}, port={{ port }})
