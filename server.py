from flask import render_template, Flask, send_from_directory, redirect, \
    url_for, jsonify, request, abort
import logging
from models import Check

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    filename='/tmp/checkme.log',
    format='%(asctime)s %(name)s %(levelname)s %(message)s'
)


@app.route('/')
def page(page=None):

    return render_template('index.html'.format(page))


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(
        'static',
        filename
    )


@app.route('/get')
def get():
    checks = Check.select().where(Check.status == 'P')
    return jsonify({'data': [x.to_json() for x in checks]})


@app.route('/get/<int:checkId>')
def get_check(checkId):
    return jsonify({'data': Check.get(id=checkId).to_json()})


@app.route('/check/<int:checkId>/<int:check>')
def set_check(checkId, check):
    c = Check.get(id=checkId)
    c.check = bool(check)
    c.save()
    return jsonify({'status': 'OK'})


@app.route('/cross/<int:checkId>/<int:cross>')
def set_cross(checkId, cross):
    c = Check.get(id=checkId)
    c.cross = bool(cross)
    c.save()
    return jsonify({'status': 'OK'})


@app.route('/new/<text>')
def new(text):
    c = Check(text=text)
    c.save()
    return jsonify({'status': 'OK'})


@app.route('/archive')
def archive():
    Check.archive()
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
