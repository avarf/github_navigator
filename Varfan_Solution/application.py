#!/usr/bin/env python

"""
    GitHub navigator
    
    Author: Ali Varfan
    Contact information: varfanm@live.com
"""

from __future__ import print_function

from flask import Flask, render_template, request
import requests
import json
import datetime


app = Flask(__name__)

@app.route("/navigator", methods=['GET', 'POST'])
def navigator():
    search_term = request.args.get('search_term', type=str)

    if search_term=="":
        return render_template('template.html', search_term="Please insert a search_term")

    commitheaders = {'Accept': 'application/vnd.github.cloak-preview'}
    query_url = "https://api.github.com/search/repositories?q="+search_term+"&sort=updated_at&order=desc"
    q_answer = requests.get(query_url).json()

    if len(q_answer['items']) < 1:
        search_term = search_term + " not found"
        return render_template('template.html', search_term=search_term)
    
    first5 = q_answer['items'][0:5]
    q_result = list()
    one_repository = dict()
    repo_id = 1

    for item in first5:
        one_repository['ID'] = repo_id
        one_repository['respository_name'] = item['name']
        one_repository['created_at'] = datetime.datetime.strptime(item['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        one_repository['owner_url'] = item['owner']['html_url']
        one_repository['avatar_url'] = item['owner']['avatar_url']
        one_repository['owner_login'] = item['owner']['login']

        # Get query for the commits
        full_name = item['full_name']
        commiturl = "https://api.github.com/repos/"+full_name+"/commits?per_page=1"
        commit_query_answer = requests.get(commiturl, headers=commitheaders).json()
        first_commit = commit_query_answer[0]
        one_repository['sha'] = first_commit['sha']
        one_repository['commit_message'] = first_commit['commit']['message']
        one_repository['commit_author_name'] = first_commit['commit']['author']['name']

        q_result.append(one_repository.copy())
        repo_id += 1
    
    return render_template('template.html', search_term=search_term, query_result=q_result)


if __name__ == "__main__":
    app.run()