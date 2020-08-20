from app import app, db
from flask import render_template, url_for, flash, get_flashed_messages, redirect, request
from datetime import datetime
from flask import Flask, session, g
import os
import models
import forms
app.secret_key = os.urandom(24)


@app.route('/base')
def base():
    return render_template('/base.html')


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
    if g.user:
        return render_template('Protected.html',user=session['user'])
    return redirect(url_for('Login'))


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
    return render_template('About.html')





@app.route('/Job')

def Job():
    tasks= models.Task.query.all()
    return render_template('Job.html', tasks=tasks, user=session['user'])


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = forms.AddTaskForm()
    if form.validate_on_submit():
        task = models.Task(title=form.title.data, date=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
        flash('Task added')
        return redirect(url_for('Job'))
    return render_template('add.html', form=form,  user=session['user'])


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
        return render_template('edit.html', form=form, task_id=task_id,user=session['user'])
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
        return render_template('delete.html', form=form, task_id=task_id, title=task.title ,user=session['user'])
    flash(f'Task with id {task_id} does not exit')
    return redirect(url_for('Job'))
