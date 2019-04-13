from flask import Flask,render_template, url_for, request, redirect, flash, session
from wtforms import Form, validators, StringField, PasswordField, RadioField
from database import connections
import gc
from passlib.hash import sha256_crypt


app=Flask(__name__)
app.secret_key="you are awesome"


class Registration(Form):
    name= StringField('Name', [validators.data_required(), validators.Length(min=5, max=50)])
    username= StringField('Username', [validators.data_required(), validators.Length(min=5, max=50)])
    password= PasswordField('Password', [validators.data_required(), validators.Length(min=5, max=50)])
    confirm_password= PasswordField('Confirm Password', [validators.data_required(), validators.Length(min=5, max=50),validators.EqualTo('password','PASSSword doesnt match')])
    gender= RadioField('Gender', choices=[('male','Male'), ('female','Female'),('others', 'Others')])
    email= StringField('Email', [validators.data_required(), validators.Length(min=5, max=50)])

class Login(Form):
    username=StringField('username')
    password=PasswordField('password')

@app.route('/')
@app.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html', title='Dashboard')


@app.route('/login',methods=['GET', 'POST'])
def login():
    try:
        c, conn = connections()
        form=Login(request.form)
        if request.method=='POST':
            username = request.form['username']
            password = sha256_crypt.encrypt(request.form['password'])
            c.execute("SELECT * FROM register_users where username =(%s)", (username,))

            data1=c.fetchone()[3]
            print(data1)
            if sha256_crypt.verify(request.form['password'], data1):
                session['loggedin']=True
                flash("!! Successfully Logged In !!")
                return redirect(url_for('dashboard'))

            else:
                session['loggedin']=False
                flash("!! Invalid Login Credential !! ")
                return redirect(url_for('login'))

    except Exception as e:
        flash("!! Invalid Login Credential !! ")
        return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)




@app.route('/register', methods=['GET', 'POST'])
def register():
        form = Registration(request.form)
        c,conn=connections()
        if request.method== "POST" and form.validate():
            name=request.form['name']
            username=request.form['username']
            password=sha256_crypt.encrypt(request.form['password'])
            gender=request.form['gender']
            email=request.form['email']

            c.execute('SELECT * FROM register_users WHERE username =(%s)', (username,))
            x=c.fetchall()
            if x:
                flash('!! User Already Exist !!')
                return redirect(url_for("register"))
            else:
                c.execute('INSERT INTO register_users (`name`,username,password,gender,email) VALUES (%s,%s,%s,%s,%s)',(name,username,password,gender,email))
                conn.commit()
                c.close()
                conn.close()
                gc.collect()
                flash('THANK YOU !! You Have Been Registered. !!')
                return redirect(url_for("dashboard"))

        return render_template('register.html', title='Signup', form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='Tushar')


app.run(debug=True)



