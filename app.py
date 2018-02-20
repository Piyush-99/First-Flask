#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 18:36:30 2018

@author: piyush
"""

from flask import Flask, render_template
from data import Articles

Articles = Articles()

app = Flask(__name__)
"""app.debug = True"""
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

if __name__ == '__main__':
    app.run(debug=True)