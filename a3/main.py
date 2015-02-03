from flask import Flask, request, render_template, redirect, url_for, jsonify
import urllib2, json
from google.appengine.ext import ndb

import models, controllers


app = Flask(__name__)
app.config['DEBUG'] = True



#routes

@app.route('/', methods=['GET', 'POST'])
def homePage():

  allGames = controllers.getAllGamesDict()
  allUsers = controllers.getAllUsersDict()
  return render_template('index.html', games=allGames, users=allUsers)
  #return redirect(url_for('.handleGameRequest'))
  #return "home"

@app.route('/users/<int:uid>/', methods=['GET', 'POST', 'DELETE'])
def showUser(uid):
  if request.method == 'DELETE':
    return json.dumps(controllers.handleDeleteUserRequest(uid))
  else:
    resp = controllers.handleGetUserRequest(uid)
    if 'errorMessage' in resp:
      return redirect(url_for('.handleUserRequest'))
    else:
      return json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': '))


@app.route('/games/<int:gid>/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def showGame(gid):
  if request.method == 'PUT':
    fkey =list(set(request.form))
    fields = {key : request.form[key] for key in fkey}
    fields['gid'] = int(gid)
    fields['uid'] = int(fields['uid'])
    return json.dumps(controllers.handleAddGuessRequest(fields), sort_keys=True, indent=4, separators=(',', ': '))
  elif request.method == 'DELETE':
    return json.dumps(controllers.handleDeleteGameRequest(gid), sort_keys=True, indent=4, separators=(',', ': ')) 
  else:
    resp = controllers.handleGetGameRequest(gid)
    if 'errorMessage' in resp:
      return redirect(url_for('.handleGameRequest'))
    else:
      return json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': '))


@app.route('/users/', methods=['GET', 'POST'])
def handleUserRequest():
  if request.method == 'POST':
    return json.dumps(controllers.handleCreateUserRequest(request.form), sort_keys=True, indent=4, separators=(',', ': '))
  else:
    return json.dumps(controllers.getAllUsersDict(), sort_keys=True, indent=4, separators=(',', ': '))


@app.route('/games/', methods=['GET', 'POST', 'PUT'])
def handleGameRequest():
  if request.method == 'POST':
    return json.dumps(controllers.handleCreateGameRequest(request.form), sort_keys=True, indent=4, separators=(',', ': '))
  elif request.method == 'PUT':
    fkey =list(set(request.form))
    fields = {key : request.form[key] for key in fkey}
    fields['gid'] = int(fields['gid'])
    fields['uid'] = int(fields['uid'])
    return json.dumps(controllers.handleAddGuessRequest(fields), sort_keys=True, indent=4, separators=(',', ': '))
  else: 
    return json.dumps(controllers.getAllGamesDict(), sort_keys=True, indent=4, separators=(',', ': '))

@app.route('/runme', methods=['GET', 'POST'])
def runMe():
  '''
  fields = {'nickName' : 'Mary3', 'email' : 'mary3@email.com'}
  newData = controllers.createUser(fields)
  mid = newData.id()
  s = json.dumps(controllers.getUser(mid))
  fields = {  'uid1' : '5066549580791808',
              'uid2' : '5629499534213120'
  }
  s = str(controllers.addGuess(5348024557502464, 5066549580791808, 0, 0, 'cat'))
  s = s + str(controllers.addGuess(5348024557502464, 5629499534213120, 0, 0, 'frat'))
  s = s + str(controllers.addGuess(5348024557502464, 5066549580791808, 0, 0, 'mat'))
  #s = str(controllers.createGame(fields))
  #alice = controllers.createUser({'nickName' : 'Alice', 'email' : 'alice@gmail.com'})
  stacy = controllers.createUser({'nickName' : 'Stacy H', 'email' : 'stacy001@gmail.com'})
  walt = controllers.createUser({'nickName' : 'Walter', 'email' : 'walt001@gmail.com'})
  joe = controllers.createUser({'nickName' : 'Joe', 'email' : 'joe@joe.com'})

  game1 = controllers.createGame({'uid1': alice.id(), 'uid2' : stacy.id()})
  game2 = controllers.createGame({'uid1': stacy.id(), 'uid2' : walt.id()})

  s = json.dumps(controllers.getAllUsersDict())
  s = str(controllers.getGamesByPlayerNamesUnion('Stacy H', 'Walter'))
  p1 = controllers.getUserByName('Bob')
  p2 = controllers.getUserByName('Alice')
  newGame = controllers.createGame({'uid1' : p1, 'uid2' : p2})
  gid = int(newGame.id())

  controllers.addGuess(gid, p1, 'dog')
  controllers.addGuess(gid, p2, 'fog')
  controllers.addGuess(gid, p1, 'log')
  controllers.addGuess(gid, p2, 'bog')
  controllers.addGuess(gid, p1, 'jog')
  controllers.addGuess(gid, p2, 'cog')

  '''

  s = str(gid)

  s = '--'
  return s + "\n<br>disabled"

  '''
@app.route('/dumprequest/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def dumpRequest():
  s = str(request.method)
  d = str(request.form)
  fkey =list(set(request.form))
  fields = {key : request.form[key] for key in fkey}
  #d['uid'] = int(d['uid'])
  s = s + str(d3)
  for key, val in request.headers.iteritems():
    s = s + "<br>\n" + key + " => " + val
  #s = s + str(request.headers)
  return s
'''

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404