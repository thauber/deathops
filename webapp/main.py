#!/usr/bin/env python2

import gevent.monkey
gevent.monkey.patch_all()

import datetime
import gevent
import json
import logging
import services.analytics
import sys

from flask import Flask, request, Response
from werkzeug.exceptions import HTTPException

log = logging.getLogger(__name__)

app = Flask(__name__)

app.config.update({
    'SECRET_KEY': '234ff7bf5cc3b5bc7af225d32c82b114',
})

# allow routes to match with a trailing slash
app.url_map.strict_slashes = False

@app.after_request
def after_request(response):
    sys.stderr.flush()
    sys.stdout.flush()
    return response

@app.errorhandler(Exception)
def catch_all(e):
    log.exception('Caught Exception: %s\n' % (e))
    if app.debug:
        raise  # this will trigger the debugger
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    msg = 'There was an error performing your request %r' % (str(e))
    return flask.Reponse(msg, code)

@app.errorhandler(400)
def invalid(e):
    msg = u'Invalid request:  %s\n    Headers:  %r\n    Body:  %r'
    log.warning(msg, request.path, request.headers, request.get_data())
    return Response(msg, 400)

@app.errorhandler(404)
def page_not_found(e):
    msg = u'Page not found'
    return Response(msg, 404)

@app.route('/e', methods=['POST'])
def event():
    if request.json:
        evt = dict(request.json)
        gevent.spawn(services.analytics.insert_events, [evt])
    return Response(u'ok\n', 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
