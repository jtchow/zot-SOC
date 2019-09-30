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

class NameForm(FlaskForm):
    degreeworks = TextAreaField(label='',validators=[DataRequired()], render_kw={"rows": 30, "cols": 90})
    submit = SubmitField('Submit')
    



@app.route('/', methods=['GET','POST'])             #if the url is zotsoc.appspot.com/ then show the form and have them enter input for my function and then display necessary classes
def index():
    form = NameForm()
    if form.validate_on_submit():
        degreeworks = form.degreeworks.data
        courses = read_input(degreeworks)
        return render_template('index1.html',courses=courses)
    return render_template('form1.html',form=form)


