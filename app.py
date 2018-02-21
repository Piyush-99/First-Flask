#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:36:30 2018

@author: piyush
"""

from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from data import Articles

from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='')

Articles = Articles()

app = Flask(__name__)
"""app.debug = True"""

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'myflask'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html',articles = Articles)

@app.route('/articles/<string:id>/')
def article(id):
    return render_template('article.html',id = id)

class RegisterForm(Form):
    name = StringField('Name',[validators.Length(min=1,max=50)])
    username = StringField('Username',[validators.Length(min=4,max=25)])
    email = StringField('Email',[validators.Length(min=6,max=50)])
    password = PasswordField('Password',[
            validators.DataRequired(),
            validators.EqualTo('confirm',message='Password dp not match')
            ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def regster():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        cur = conn.cursor()
     
        cur.execute('INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)',(name, email, username,password))
        
        conn.commit()
        
        cur.close()
            
        flash('You are now registered and can log in','success')
        
        return redirect(url_for('index'))
        
    return render_template('register.html',form=form)

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)