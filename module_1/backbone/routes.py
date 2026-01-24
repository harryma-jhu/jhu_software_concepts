from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/projectst')
def projects():
    return render_template('projects.html')

@bp.route('/kcontact')
def contact():
    return render_template('contact.html')

