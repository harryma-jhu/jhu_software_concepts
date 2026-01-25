from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/projects')
def projects():
    return render_template('projects.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')

