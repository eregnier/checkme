from flask import render_template, Flask, send_from_directory, redirect, \
    url_for, jsonify, request, abort
import logging
from models import Check, Category

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


@app.route('/get/check/<int:categoryId>')
def get_check(categoryId):
    checks = Check.select().where(
        (Check.status == 'P') & (Check.category == categoryId)
    )
    return jsonify({'data': [x.to_json() for x in checks]})


@app.route('/get/category')
def get_category():
    return jsonify({'data': [x.to_json() for x in Category.select()]})


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


@app.route('/new/check/<int:categoryId>/<text>')
def new_check(categoryId, text):
    Check(
        text=text,
        category=Category.get(id=categoryId)
    ).save()
    return jsonify({'status': 'OK'})


@app.route('/new/category/<text>')
def new_category(text):
    Category(text=text).save()
    return jsonify({'status': 'OK'})


@app.route('/archive/<int:categoryId>')
def archive(categoryId):
    Check.archive(categoryId)
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
