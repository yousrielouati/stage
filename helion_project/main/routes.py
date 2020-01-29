from flask import Blueprint, render_template,redirect,url_for ,session

main = Blueprint('main' , __name__)

from app import is_logged_in



@main.route('/dashboard')
@is_logged_in
def dashboard():
        return render_template('dashboard.html')
