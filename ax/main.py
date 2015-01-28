from flask import Flask, request, render_template, redirect, url_for, make_response
import urllib2
from google.appengine.ext import ndb

import models, views, controllers

app = Flask(__name__)
app.config['DEBUG'] = True

#routes

@app.route('/', methods=['GET', 'POST'])
def basic():
  return render_template('index.html')
  #return make_response(open('templates/rendered.html').read())

@app.route('/view', methods=['GET', 'POST'])
def displayData():
  d = controllers.fetchAllCardObjects();
  tableRows = views.makeReadOnlyTableRows(d)
  return render_template('dataTable.html', readOnlyTable=tableRows)

@app.route('/edit', methods=['GET', 'POST'])
def editData():
  if request.method == "POST":
    controllers.chooseAction(request.form)
  d = controllers.fetchAllCardObjects();
  tableRows = views.makeReadOnlyTableRows(d)
  cardData = controllers.cardDict(d)
  return render_template('editor.html', readOnlyTable=tableRows, cd=cardData)

@app.route('/editCard', methods=['GET', 'POST'])
def editCard():
  msg = ""
  if request.method == "GET" and 'usk' in request.args:
    cardObject = controllers.getCardByKey(request.args['usk'])
    return render_template('editCard.html', cardObject=cardObject, usk=request.args['usk'])
  else:
    return redirect(url_for('.editData'))

@app.route('/test', methods=['GET', 'POST'])
def tester():
  out = ""
  if request.method == "POST":
    return "yep - got the post request"
  elif request.method == "GET":
    return "yep - got the get request"




@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404