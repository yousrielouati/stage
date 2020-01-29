from flask import Flask,session,redirect,url_for,flash
from flask_mysqldb import MySQL
from flask_session import Session
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
sess = Session()
byc = Bcrypt(app)

app.config.from_pyfile('config.py')

mysql = MySQL(app)


from users.routes import users
app.register_blueprint(users)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs) :
        if 'loggedin' in session :
            return f(*args,**kwargs)
        else:
            flash("acces denied , login needed ")
            return redirect(url_for('users.login'))
    return wrap


from main.routes import main
app.register_blueprint(main)


if __name__ == '__main__' :
    sess.init_app(app)
    app.run()
