from app import app, db
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from flask import render_template, url_for, flash, get_flashed_messages, redirect, request
from datetime import datetime
from flask import Flask, session, g
import os
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash,check_password_hash
from flask_wtf import FlaskForm
import models
from wtforms import StringField ,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length
import forms

app.secret_key = os.urandom(24)
Bootstrap(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view ='logged'

class RegistrationForm(FlaskForm):
    email = StringField('email',validators=[InputRequired(),Email(message='Invalid_email'),Length(max=50)])
    username = StringField('username',validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])
    

class LoginForm(FlaskForm):
    username = StringField('username',validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])
    remember = BooleanField('remember me')

class info(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15),unique=True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(50))

@login_manager.user_loader
def Load_user(user_id):
    return info.query.get(int(user_id))



@app.route('/')

@app.route('/base')

def base():
    return render_template('/base.html', )


@app.route('/index')
def index():
    return render_template('/index.html')    

@app.route('/register' ,methods=['GET','POST'])
def  register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data,method="sha256")
        new_register = info(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(new_register)
        db.session.commit()
        return render_template('/logged.html',form=form)
       # return '<h1>'+ form.username.data+''+form.password.data+''+form.email.data+'</h1>'
    return render_template('/register.html', form=form)



@app.route('/logged',methods=['GET','POST'])
def logged():
    form= LoginForm()

    if form.validate_on_submit():
        user = info.query.filter_by(username=form.username.data).first()
        if user:
            if  check_password_hash(user.password,  form.password.data):
                login_user(user,remember=form.remember.data)
                return redirect(url_for('Protected'))

        return '<h1> invalid user name </h1>'       
    return render_template('/logged.html',form=form)  


@app.route('/Login',methods=['GET','POST'])
def Login():
    if request.method =='POST':
        session.pop('user',None)
        
        if request.form['password'] == "123":
            session['user'] = request.form['username']
            return redirect(url_for('Protected'))
   
    return render_template('Login.html')

@app.route('/Protected')
def Protected():  
    #if g.user:
    return render_template('Protected.html', name=current_user.username)
    #return redirect(url_for('Login'))



@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']

@app.route('/dropsession')

def dropsession():
    session.pop('user',None)
    return render_template('base.html')

@app.route('/About')
def About():
    return render_template('About.html' )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base'))


@app.route('/User')
def User():
    return render_template("/User.html")



@app.route('/Job')
@login_required
def Job():
    tasks= models.Task.query.all()
    return render_template('Job.html', tasks=tasks,name=current_user.username)
    return redirect(url_for('logged'))



@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = forms.AddTaskForm()
    if form.validate_on_submit():
        task = models.Task(title=form.title.data, date=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        flash('Task added')
        return redirect(url_for('Job'))
    return render_template('add.html', form=form,name=current_user.username)
    return redirect(url_for('Logged'))



@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    form = forms.AddTaskForm()
    task = models.Task.query.get(task_id)
    print(task)
    if task:
        if form.validate_on_submit():
            task.title = form.title.data
            task.date = datetime.utcnow()
            db.session.commit()
            flash('Task updated')
            return redirect(url_for('Job'))
        form.title.data = task.title
        return render_template('edit.html', form=form, task_id=task_id,name=current_user.username)
    flash(f'Task with id {task_id} does not exit')
    return redirect(url_for('Job'))


@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    form = forms.DeleteTaskForm()
    task = models.Task.query.get(task_id)
    if task:
        if form.validate_on_submit():
            if form.submit.data:
                db.session.delete(task)
                db.session.commit()
                flash('Task deleted')
            return redirect(url_for('Job'))
        return render_template('delete.html', form=form, task_id=task_id, title=task.title,name=current_user.username)
    flash(f'Task with id {task_id} does not exit')
    return redirect(url_for('Job'))
