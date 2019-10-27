# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 01:36:45 2019

@author: Jason
"""
from input_reader import *
from flask import Flask, render_template,request



app = Flask(__name__)   #initialize flask app              
app.config['SECRET_KEY'] = 'hard to guess string'             
   



@app.route('/')             #if the url is zotsoc.appspot.com/ then show the form and have them enter input for my function and then display necessary classes
def index():
    return render_template('homepage.html')

    

@app.route('/', methods=['POST'])
def show_output():
    degreeworks = request.form['degreeworks']
    courses = read_input(degreeworks)
    return render_template('results.html',courses=courses)


