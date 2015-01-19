from google.appengine.ext import ndb
import models
import json

def chooseAction(fields):
  if 'behavior' in fields:
    if fields['behavior'] == 'addNewCard':
      addCardtoDB(fields)
    elif fields['behavior'] == 'editExistingCard':
      saveEdits(fields)

def addCardtoDB(fields):
  if newCardHasAllRequired(fields):
    k = ndb.Key(models.cardObject, "default-group")
    newCard = models.cardObject(parent=k)
    newCard.cardType = fields['cardType']
    newCard.cardName = fields['cardName']
    if 'inBaseDeck' in fields and fields['inBaseDeck'] == 'on':
      newCard.includedIn = ["base"]
    if 'cardDesc' in fields and len(fields['cardDesc']) > 0:
      newCard.cardDesc = fields['cardDesc']
    if 'newCardTags' in fields and len(fields['newCardTags']) > 0:
      newCard.cardTags = fields['newCardTags'].lower().split(",")
    #save card
    newCard.put() 

def updateCardinDB(usk, fields):
  cardObj = getCardObject(usk)
  if 'includedIn' in fields:
    cardObj.includedIn = fields['includedIn']
  if 'cardName' in fields:
    cardObj.cardName = fields['cardName']
  if 'cardType' in fields:
    cardObj.cardType = fields['cardType']
  if 'cardDesc' in fields:
    cardObj.cardDesc = fields['cardDesc']
  if 'cardTags' in fields:
    cardObj.cardTags = fields['cardTags']
  cardObj.put()


def saveEdits(fields):
  if newCardHasAllRequired(fields):
    return True


def newCardHasAllRequired(fields):
  result = False
  if ('cardType' in fields) and ('cardName' in fields):
    if len(fields['cardType']) > 0 and len(fields['cardDesc']) > 0:
      result = True
  
  return result

def fetchAllCardObjects():
  allCards = [{
  'key' : x.key.urlsafe(),
  'created_timmestamp' : x.created_timmestamp,
  'modified_timestamp' : x.modified_timestamp,
  'cardType' : x.cardType,
  'includedIn' : x.includedIn,
  'cardName' : x.cardName,
  'cardDesc' : x.cardDesc,
  'cardTags' : x.cardTags,
  'addedBy' : x.addedBy,
  'modifiedBy' : x.modifiedBy
  } for x in models.cardObject.query(ancestor=ndb.Key(models.cardObject, "default-group")).fetch()]
  return allCards

def cardDict(allCards):
  cd = dict()
  for card in allCards:
    cd[card['key']] = card
  return cd

def getCardObject(cardKey):
  rev_key = ndb.Key(urlsafe=cardKey)
  x = rev_key.get()
  return x

def getCardByKey(cardKey):
  rev_key = ndb.Key(urlsafe=cardKey)
  x = rev_key.get()
  base = False
  if ('base' in set(x.includedIn)):
    base = True
  #x = models.cardObject.query(ndb.Key(urlsafe=cardKey)).fetch()
  cardDict = {
  'key' : x.key.urlsafe(),
  'created_timmestamp' : x.created_timmestamp,
  'modified_timestamp' : x.modified_timestamp,
  'cardType' : x.cardType,
  'includedIn' : base,
  'cardName' : x.cardName,
  'cardDesc' : x.cardDesc,
  'cardTags' : ",".join(x.cardTags),
  'addedBy' : x.addedBy,
  'modifiedBy' : x.modifiedBy
  }
  return cardDict



def getDiffs(form, remote):
  diffs = dict()
  #cardType
  if form['cardType'].lower() != remote['cardType'].lower():
    diffs['cardType'] = form['cardType']
  #inBaseDeck
  if 'inBaseDeck' in form and form['inBaseDeck'] == 'on':
    if remote['includedIn'] == False:
      diffs['includedIn'] = ["base"] 
  elif 'inBaseDeck' not in form:
    if remote['includedIn'] == True:
      diffs['includedIn'] = []
  #cardName
  if form['cardName'].lower() != remote['cardName'].lower():
    diffs['cardName'] = form['cardName']
  #cardDesc
  if form['cardDesc'].lower() != remote['cardDesc'].lower():
    diffs['cardDesc'] = form['cardDesc']
  #cardTags
  formTags = set(form['cardTags'].lower().split(","))
  remoteTags = set(remote['cardTags'].lower().split(","))
  if len(formTags.symmetric_difference(remoteTags)) > 0:
    diffs['cardTags'] = list(formTags)
  return diffs



def getItems():
  fetchedQuery = models.cardObject.query(ancestor=ndb.Key(models.cardObject, "default-group")).fetch()
  d = [{'key' : x.key.urlsafe(), 'cName' : x.cardName} for x in fetchedQuery]
  e = []
  for item in d:
    cardKey = ndb.Key(urlsafe=item['key'])
    card = cardKey.get()
    e.append(card.cardName)

  return e