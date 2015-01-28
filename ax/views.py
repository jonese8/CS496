import models, controllers

def makeReadOnlyTableRows(d):
  tableRows = []
  for row in d:
    card = dict()
    card['urlsafekey'] = row['key']
    card['cardType'] = row['cardType']
    if 'base' in  set(row['includedIn']):
      card['includedIn'] = True
    else:
      card['includedIn'] = False

    card['cardName'] = row['cardName']
    card['cardDesc'] = row['cardDesc']
    card['cardTags'] = row['cardTags']

    #add to tableRows
    tableRows.append(card)
  #return all the rows 
  return tableRows






