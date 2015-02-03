from google.appengine.ext import ndb
import models
import json

def createUser(fields):
 if 'nickName' in fields:
  newUser = models.User(nickName=fields['nickName'])
  if 'email' in fields:
    newUser.email = fields['email']
  return newUser.put()

def createGame(fields):
  if ('uid1' in fields and 'uid2' in fields):
    p1 = ndb.Key(models.User, int(fields['uid1'])).get()
    p2 = ndb.Key(models.User, int(fields['uid2'])).get()
    if len(p1.nickName) > 0 and len(p2.nickName) > 0:
      newGame = models.Game(playerNames = [p1.nickName, p2.nickName])
      ngk = newGame.put()
      p1.numGamesPlayed += 1
      p2.numGamesPlayed += 1
      p1.put()
      p2.put()

      return ngk

def handleGetUserRequest(uid):
  if ndb.Key(models.User, int(uid)).get() is None:
    return {'errorMessage' : 'unable to find uid \'' + str(uid) + '\' in database'}
  else:
    return getUserDict(int(uid))

def handleGetGameRequest(gid):
  if ndb.Key(models.Game, int(gid)).get() is None:
    return {'errorMessage' : 'unable to find gid \'' + str(gid) + '\' in database'}
  else:
    return getGameDict(int(gid))

def handleCreateUserRequest(fields):
  if 'nickName' in fields:
    #check if name is available
    if len(str(getUserByName(fields['nickName']))) == 0:
      newUser = createUser(fields)
      return {'newUser' : newUser.id()}
    else:
      return {'errorMessage' : 'specified nickName already in use'}
  else:
    return {'errorMessage' : 'unique nickName data field required to create new user'}

def handleCreateGameRequest(fields):
  #check for both uid1, uid2
  if ('uid1' in fields and 'uid2' in fields):
    #check that uid1 is an existing player
    #check that uid2 is an existing player
    u1 = getUser(int(fields['uid1']))
    u2 = getUser(int(fields['uid2']))
    if (u1 is None) or (len(str(u1)) == 0):
      return {'errorMessage' : 'uid1 \'' + str(fields['uid1']) + '\' not found in user database'}
    elif (u2 is None) or (len(str(u2)) == 0):
      return {'errorMessage' : 'uid2 \'' + str(fields['uid2']) + '\' not found in user database'}
    else: 
      newGame = createGame(fields)
      return {'newGame' : newGame.id()}

  else:
    return {'errorMessage' : 'valid user ids labeled as uid1, uid2 are required to create a new game'}

def handleAddGuessRequest(fields):
  #check for necessary fields
  #check for user in game
  #if round is partial, make sure hasn't already guessed
  if ('uid' in fields and 'guess' in fields and 'gid' in fields):
    if playerIsInGame(int(fields['uid']), int(fields['gid'])):
      if playerFreeToMove(int(fields['uid']), int(fields['gid'])):
        updatedGame = addGuess(fields['gid'], fields['uid'], fields['guess'])
        return {'updatedGame' : updatedGame.id()}
      else:
        return {'errorMessage' : 'player may not move twice in the same round'}      
    else:
      return {'errorMessage' : 'invalid game or player and game combination'}
  else:
    return {'errorMessage' : 'guess requires valid uid, gid, and guess'}

def handleDeleteUserRequest(uid):
  if ndb.Key(models.User, int(uid)).get() is None:
    return {'errorMessage' : 'unable to find uid \'' + str(uid) + '\' in database'}
  else:
    removeUser(uid)
    return {'removedUser' : uid}

def handleDeleteGameRequest(gid):
  if ndb.Key(models.Game, int(gid)).get() is None:
    return {'errorMessage' : 'unable to find gid \'' + str(gid) + '\' in database'}
  else:
    deleteGame(gid)
    return {'removedGame' : gid}

def removeUser(uid):
  thisUser = ndb.Key(models.User, int(uid)).get().key
  return thisUser.delete()

def deleteGame(gid):
  thisGame = ndb.Key(models.Game, int(gid)).get().key
  return thisGame.delete()

def playerIsInGame(uid, gid):
  status = False
  thisGame = getGame(gid)
  if not(thisGame is None):
    #if no rounds, compare names
    #else compare uid to uid of firstGuess
    #or compare uid to uid of secondGuess if partial == false
    playerNames = list(thisGame.playerNames)
    thisUser = getUser(uid)
    if not(thisUser is None):
      if thisUser.nickName in playerNames:
        status = True
  return status

def playerFreeToMove(uid, gid):
  status = False
  if playerIsInGame(uid, gid):
    thisGame = getGame(gid)
    roundCount = len(thisGame.rounds)
    if roundCount == 0:
      status = True
    elif thisGame.rounds[roundCount - 1].partial == False:
      status = True
    elif thisGame.rounds[roundCount - 1].firstGuess.playerID != int(uid):
      status = True
  return status

def checkValidGameAndUsers(gid, uid1, uid2):
  if (playerIsInGame(uid1, gid) and playerIsInGame(uid2, gid)):
    return True
  else:
    return False

def getBackLinksFromLastRound(gid, uid):
  thisGame = getGame(gid)

  if thisGame:
    roundCount = len(thisGame.rounds)
    if roundCount == 0 or (roundCount == 1 and thisGame.rounds[0].partial == True):
      return ["", ""]
    else:
      if thisGame.rounds[roundCount - 1].partial == False:
        parentRound = thisGame.rounds[roundCount - 1]
      else:
        parentRound = thisGame.rounds[roundCount - 2]
      if parentRound.firstGuess.playerID == uid:
        firstGuess = parentRound.firstGuess.word
        secondGuess = parentRound.secondGuess.word
        return [firstGuess, secondGuess]
      elif parentRound.secondGuess.playerID == uid:
        firstGuess = parentRound.secondGuess.word
        secondGuess = parentRound.firstGuess.word
        return [firstGuess, secondGuess]
      else:
        return ['-error-', '-error-']

def addGuess(gid, uid, guess):
  if checkValidGameAndUsers(gid, uid, uid):
    bl = getBackLinksFromLastRound(gid, uid)
    prev1 = bl[0]
    prev2 = bl[1]
    newGuess = models.Guess(playerID=uid, word=guess, backLink1=prev1, backLink2=prev2)
    thisGame = getGame(gid)
    roundCount = len(thisGame.rounds)
    #check the highest index for partial
    if roundCount == 0 or thisGame.rounds[roundCount - 1].partial == False:
      #create new round and flip partial
      newRound = models.Round(roundNum=roundCount, firstGuess=newGuess, partial=True)
      thisGame.rounds.append(newRound)
    else:
      thisRound = thisGame.rounds[roundCount - 1]
      thisRound.secondGuess = newGuess
      thisRound.partial=False
      if str(thisRound.firstGuess.word).lower() == str(guess).lower():
        thisGame.convergenceStatus = True
    return thisGame.put()

def getUser(uid):
  return ndb.Key(models.User, int(uid)).get()

def getGame(gid):
  return ndb.Key(models.Game, int(gid)).get()

def getUserByName(uname):
  foundUsers = models.User.query(models.User.nickName==uname).fetch()
  if len(foundUsers) > 0:
    return foundUsers[0].key.id()
  else: 
    return ""

def getGamesByPlayerNamesUnion(uname1, uname2):
  foundGames = models.Game.query(models.Game.playerNames==uname1 or models.Game.playerNames==uname1).fetch()
  if len(foundGames) > 0:
    return [x.key.id() for x in foundGames]
  else:
    return ""

def getGamesByPlayerNamesIntersection(uname1, uname2):
  foundGames = models.Game.query(models.Game.playerNames==uname1 and models.Game.playerNames==uname1)
  if len(foundGames) > 0:
    return [x.key.id for x in foundGames]
  else:
    return []

def getUserDict(uid):
  userDict = ndb.Key(models.User, int(uid)).get().to_dict()
  return userDict

def getGameDict(gid):
  gameDict = ndb.Key(models.Game, int(gid)).get().to_dict()
  return gameDict

def getAllUsersDict():
  userList = [x.to_dict() for x in models.User.query().fetch()]
  return userList

def getAllGamesDict():
  gameList = [x.to_dict() for x in models.Game.query().fetch()]
  return gameList

