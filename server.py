import logging
from flask import render_template, Flask, send_from_directory, jsonify
from flask_login import login_required, current_user
from flask_classy import FlaskView, route
from models.check import Check
from models.category import Category
from auth import register_auth

app = Flask(__name__)


logging.basicConfig(
    level=logging.INFO,
    filename='/tmp/checkme.log',
    format='%(asctime)s %(name)s %(levelname)s %(message)s'
)


class MainView(FlaskView):

    @login_required
    def index(self):
        return render_template('index.html', current_user=current_user)

    @route('/static/<path:filename>')
    @login_required
    def serve_static(self, filename):
        return send_from_directory(
            'static',
            filename
        )


class CheckView(FlaskView):

    @login_required
    def get(self, categoryId):
        checks = Check.select().where(
            (Check.status == 'P') & (Check.category == int(categoryId))
        )
        return jsonify({'data': [x.to_json() for x in checks]})

    @login_required
    def check(self, checkId, check):
        c = Check.get(id=int(checkId))
        c.check = True if check == '1' else False
        c.save()
        return jsonify({'status': 'OK'})

    @login_required
    def cross(self, checkId, cross):
        c = Check.get(id=int(checkId))
        c.cross = True if cross == '1' else False
        c.save()
        return jsonify({'status': 'OK'})

    @login_required
    def new(self, categoryId, text):
        Check(
            text=text,
            category=Category.get(id=int(categoryId))
        ).save()
        return jsonify({'status': 'OK'})

    @login_required
    def archive(self, categoryId):
        Check.archive(int(categoryId))
        return jsonify({'status': 'OK'})

    @login_required
    def priority(self, checkId, priority):
        check = Check.get(id=int(checkId))
        check.priority = int(priority)
        check.save()
        return jsonify({'status': 'OK'})


class CategoryView(FlaskView):

    @login_required
    def all(self):
        categories = Category.select().where(Category.user == current_user.id)
        return jsonify({'data': [x.to_json() for x in categories]})

    @login_required
    def new(self, text):
        Category(text=text, user=current_user.id).save()
        return jsonify({'status': 'OK'})


MainView.register(app)
CheckView.register(app)
CategoryView.register(app)

register_auth(app)

app.config["SECRET_KEY"] = 'Super Check Admin Key'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
