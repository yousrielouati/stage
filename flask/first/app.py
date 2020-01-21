from flask import Flask, render_template , request, redirect ,url_for,session
from flask_mysqldb import MySQL
app = Flask(__name__)
app.debug = True


# config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'testingdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

#login
@app.route('/',methods=['GET','POST'])
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
            return redirect(url_for("dashboard"))
        else:
            msg ="authentification error , please try again "
            cur.close()
            return render_template('login.html', message = msg)
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # test if logged in
        if session["loggedin"] :
             return render_template('dashboard.html')
        else :
            return render_template("login.html")


@app.route('/edit',methods=['GET','POST'])
def edit():
    # test if logged in
    if session["loggedin"]:
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
            return redirect(url_for("dashboard"))

        return render_template('edit.html')
    else:
        return render_template("login.html")



@app.route('/logout')
def logout():
    # destroy session
    session.clear()
    return render_template('login.html', message = "you are now logged out")





if __name__  ==  '__main__':
    app.secret_key='secret123'
    app.run(debug=True)