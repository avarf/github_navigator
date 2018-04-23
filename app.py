#!/usr/bin/env python

from __future__ import print_function

from flask import Flask, jsonify, render_template, request, session
import requests

# not sure imports
#############################################
import ast

import json
import uuid

from flask import send_file
from flask import Response

from io import BytesIO

from os.path import expanduser
from gevent.wsgi import WSGIServer
#############################################


app = Flask(__name__)

@app.route("/")
def index():
    message = "Hello Ali"
    return render_template('home.html', message=message)


@app.route("/navigator", methods=['GET', 'POST'])
def navigator():
    search_term = request.args.get('search_term', type=str)
    return_msg = "The Search term is: " + search_term
    return render_template('home.html', message = return_msg)

@app.route('/test_query', methods=['GET','POST'])
def test_query():
    search_term = request.args.get('search_term', type=str)

    # https://api.github.com/search/repositories?q=arrow
    url = "https://api.github.com/search/repositories?q="
    query_url = url + search_term

    q_result = requests.get(query_url).json()
    print('\n')
    print('Result:\n', q_result.keys())
    print('\n')
    
    first5 = q_result['items'][0:5]
    print('\n')
    print('type(first5)', type(first5))
    print("full_names: \n")

    full_names = ""
    for item in first5:
        print(item['full_name'])
        full_names = full_names + "--" + item['full_name']
    # print('First 5:\n', first5.keys())
    print('\n')
    
    return render_template('home.html', message=full_names)

if __name__ == "__main__":
    app.run()