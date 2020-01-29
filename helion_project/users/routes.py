from flask import Blueprint, render_template , session , request , redirect , url_for

users = Blueprint('users' , __name__)

from app import mysql,  is_logged_in
#login
@users.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #get from fields
        username = request.form['username']
        password = request.form['password']
        #open cursor
        cur = mysql.connection.cursor()
        # execute
        result = cur.execute(" select * from clients where username= %s and password = %s ",(username,password))
        if result > 0 :
            # get user
            tab = cur.fetchone()
            # close cursor
            cur.close()
            # create session
            session["loggedin"] = True
            session["username"] = username
            session["id"] = tab['id']
            return redirect(url_for("main.dashboard"))
        else:
            msg ="authentification error , please try again "
            cur.close()
            return render_template('login.html', message = msg)
    return render_template('login.html')

@users.route('/edit',methods=['GET','POST'])
@is_logged_in
def edit():

        if request.method == 'POST':
            # get form field
            newpwd = request.form['newpwd']
            # create cursor
            cur = mysql.connection.cursor()
            # execute
            result = cur.execute(" update clients set password = %s where id = %s",(newpwd,session["id"]))
            # commit
            mysql.connection.commit()
            cur.close()
            return redirect(url_for("main.dashboard"))

        return render_template('edit.html')




@users.route('/logout')
@is_logged_in
def logout():
    # destroy session
    session.clear()
    return render_template('login.html', message = "you are now logged out")
