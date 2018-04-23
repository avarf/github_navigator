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

    commitheaders = {'Accept': 'application/vnd.github.cloak-preview'}

    print(type(search_term))
    query_url = "https://api.github.com/search/repositories?q="+search_term+"&sort=updated_at&order=desc"

    q_answer = requests.get(query_url).json()
    # q_answer = requests.get(query_url, headers=headers).json()

    # if q_answer.ok():
    #     pass
    # else:
    #     print("q_answer IS Wrong")
    #     return
    
    first5 = q_answer['items'][0:5]

    q_result = list()
    one_repository = dict()

    # one_repository = {
    #     respository_name: "",
    #     created_at: "",
    #     owner_url: "",
    #     avatar_url: "",
    #     owner_login: "",
    #     sha: "",
    #     commit_message: "",
    #     commit_author_name: ""
    # }

    for item in first5:
        one_repository['respository_name'] = item['name']
        one_repository['created_at'] = item['created_at']
        one_repository['owner_url'] = item['owner']['url']
        one_repository['avatar_url'] = item['owner']['avatar_url']
        one_repository['owner_login'] = item['owner']['login']

        # Get query for the commits
        full_name = item['full_name']
        # commiturl = "https://api.github.com/repos/fenjuly/ArrowDownloadButton/commits?per_page=1"
        commiturl = "https://api.github.com/repos/"+full_name+"/commits?per_page=1"
        commit_query_answer = requests.get(commiturl, headers=commitheaders).json()

        first_commit = commit_query_answer[0]

        one_repository['sha'] = first_commit['sha']
        one_repository['commit_message'] = first_commit['commit']['message']
        one_repository['commit_author_name'] = first_commit['commit']['author']['name']

        q_result.append(one_repository.copy())
        # full_names = full_names + item['full_name'] + "--"

    print('\n')
    print('Final Query Results:', q_result)
    print('\n')
    
    return render_template('template.html', search_term=search_term, query_result=q_result)


    # <h3> Created {created_at}</h3>
    # <a href="{owner_url}"><img src="{avatar_url}" alt="avatar" height="42" width="42"/></a>
    # {owner_login}
    # <h3>LastCommit</h3>
    # {sha} {commit_message}  {commit_author_name}
    # <hr/>


@app.route('/test_query2', methods=['GET', 'POST'])
def test_query2():
    qurl = "https://api.github.com/search/repositories?q=arrow&sort=updated_at&order=desc"
    
    full_name = ""
    commiturl = "https://api.github.com/repos/fenjuly/ArrowDownloadButton/commits?per_page=1"

   
    headers = {'Accept': 'application/vnd.github.mercy-preview+json'}
    commitheaders = {'Accept': 'application/vnd.github.cloak-preview'}

    # q_answer = requests.get(qurl, headers=headers).json()
    q_answer = requests.get(commiturl, headers=commitheaders).json()

    print('\n')
    print('Full Query Answer:')
    print(json.dumps(q_answer, indent=4))
    print('\n')


    first = q_answer['items'][0]

    jf = json.dumps(first, indent=4)
    # jf = json.loads(jf)
    print('\n')
    print('First item: \n')
    # print(first)
    print(jf)

    print('\n')
    # print(jf)

    print('\n')







if __name__ == "__main__":
    app.run()