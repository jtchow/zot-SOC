# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 01:36:45 2019

@author: Jason
"""
from input_reader import *
from flask import Flask, render_template,request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


app = Flask(__name__)   #initialize flask app 
bootstrap = Bootstrap(app)              #dont think i need this lol
app.config['SECRET_KEY'] = 'hard to guess string'               #or this
   



@app.route('/')             #if the url is zotsoc.appspot.com/ then show the form and have them enter input for my function and then display necessary classes
def index():
    return render_template('homepage.html')

    

@app.route('/', methods=['POST'])
def show_output():
    degreeworks = request.form['degreeworks']
    courses = read_input(degreeworks)
    return render_template('index2.html',courses=courses)


