from google.appengine.ext import ndb

class Model(ndb.Model):

  def to_dict(self):
    d = super(Model, self).to_dict()
    d['key'] = self.key.id()
    return d

class ModelT(Model):
  created_timestamp = ndb.DateTimeProperty(auto_now_add=True)
  modified_timestamp = ndb.DateTimeProperty(auto_now=True) 

  def to_dict(self):
    d = super(ModelT, self).to_dict()
    d['created_timestamp'] = str(self.created_timestamp)  
    d['modified_timestamp'] = str(self.modified_timestamp)  
    return d


class User(ModelT):
  nickName = ndb.StringProperty()  
  email = ndb.StringProperty()
  pwd = ndb.StringProperty()
  numGamesPlayed = ndb.IntegerProperty(default=0)


class Guess(ModelT):
  playerID = ndb.IntegerProperty(required=True)
  backLink1 = ndb.StringProperty(required=True)
  backLink2 = ndb.StringProperty(required=True)
  word = ndb.StringProperty(required=True)

class Round(ModelT):
  roundNum = ndb.IntegerProperty()
  firstGuess = ndb.StructuredProperty(Guess)
  secondGuess = ndb.StructuredProperty(Guess)
  partial = ndb.BooleanProperty(default=False)


class Game(ModelT):
  playerNames= ndb.StringProperty(repeated=True)
  rounds = ndb.StructuredProperty(Round, repeated=True)
  convergenceStatus = ndb.BooleanProperty(default=False)

  def to_dict(self):
    d = super(Game, self).to_dict()
    for eachRound in d['rounds']:
      eachRound['created_timestamp'] = str(eachRound['created_timestamp'])
      eachRound['modified_timestamp'] = str(eachRound['modified_timestamp'])
      if 'created_timestamp' in eachRound['firstGuess']:
        eachRound['firstGuess']['created_timestamp'] = str(eachRound['firstGuess']['created_timestamp'])
      if 'modified_timestamp' in eachRound['firstGuess']:
        eachRound['firstGuess']['modified_timestamp'] = str(eachRound['firstGuess']['modified_timestamp'])
      if eachRound['partial'] == True:
        eachRound.pop('secondGuess')
      else:
        if 'created_timestamp' in eachRound['secondGuess']:
          eachRound['secondGuess']['created_timestamp'] = str(eachRound['secondGuess']['created_timestamp'])
        if 'modified_timestamp' in eachRound['secondGuess']:
          eachRound['secondGuess']['modified_timestamp'] = str(eachRound['secondGuess']['modified_timestamp'])
    return d


'''

  created_timestamp = ndb.DateTimeProperty(auto_now_add=True)
  modified_timestamp = ndb.DateTimeProperty(auto_now=True) 

'''













