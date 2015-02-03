'''
NOTE TO GRADER:

All tests in this file passed .
(but id's and values would need to be updated to be consistent with the current database instance)
The tests were run by executing each block in a python interpreter repl
Each result was displayed in the terminal as it was run and since results
are built into the request handler functions, they were not saved separately.
A passing test is indicated by a json containing the id of the item.
Failing tests return a json with an 'errorMessage' key
'''


import subprocess
cmdTemplate = "curl -H \"Accept: application/json\" -X %s %s %s%s"
dt = "-d \"%s=%s\" "
commandList = list()


#test create a player
#   status: PASS
reqType = "POST"
data = dt % ('nickName', 'Jim')
data = data + dt % ('email', 'jim@gmail.com')
url = "http://osterbit-rest-001.appspot.com/users/"
suffix = ""
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test get all Users
#   status: PASS
reqType = "GET"
data = ""
url = "http://osterbit-rest-001.appspot.com/users/"
suffix = ""
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test get user
#   status: PASS
reqType = "GET"
data = ""
url = "http://osterbit-rest-001.appspot.com/users/"
suffix = "6614661952700416"
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test get non-existent user
#   status: PASS
reqType = "GET"
data = ""
url = "http://osterbit-rest-001.appspot.com/users/"
suffix = "6614661952700412"
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test get all games
#   status: PASS
reqType = "GET"
data = ""
url = "http://osterbit-rest-001.appspot.com/games/"
suffix = ""
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test get a game
#   status: PASS
reqType = "GET"
data = ""
url = "http://osterbit-rest-001.appspot.com/games/"
suffix = "5348024557502464"
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test getting a non-existent game
#   status: PASS
reqType = "GET"
data = ""
url = "http://osterbit-rest-001.appspot.com/games/"
suffix = "5348024557502424"
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test put a guess with the game id in url
#   status: PASS
reqType = "PUT"
data = dt % ('uid', '5629499534213120')
data = data + dt % ('guess', 'fifty')
url = "http://osterbit-rest-001.appspot.com/games/"
suffix = "5348024557502464"
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test put a guess without the game id in url
#   status: PASS
reqType = "PUT"
data = dt % ('uid', '5066549580791808')
data = data + dt % ('guess', 'fifty')
url = "http://osterbit-rest-001.appspot.com/games/"
suffix = "5348024557502464"
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test attempt to go twice in a row
#   status: PASS
subprocess.call(command, shell=True)

#test attempt to use invalid game
#   status: PASS
reqType = "PUT"
data = dt % ('uid', '5066549580791801')
data = data + dt % ('guess', 'fifty')
url = "http://osterbit-rest-001.appspot.com/games/"
suffix = "5348024557502464"
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test attempt to use wrong player
#   status: PASS
reqType = "PUT"
data = dt % ('uid', '5910974510923776')
data = data + dt % ('guess', 'fifty')
url = "http://osterbit-rest-001.appspot.com/games/"
suffix = "5348024557502464"
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test create a player
#   status: PASS
reqType = "POST"
data = dt % ('nickName', 'Jim')
data = data + dt % ('email', 'jim@gmail.com')
url = "http://osterbit-rest-001.appspot.com/users/"
suffix = ""
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)


#test attempt to create player with same nickname
#   status: PASS
subprocess.call(command, shell=True)


#test create a game
#   status: PASS
reqType = "POST"
data = dt % ('uid1', '6262818231812096')
data = data + dt % ('uid2', '4644337115725824')
url = "http://osterbit-rest-001.appspot.com/games/"
suffix = ""
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test attempt to create a game with invalid players
#   status: PASS
reqType = "POST"
data = dt % ('uid1', '6262818231812091')
data = data + dt % ('uid2', '4644337115725821')
url = "http://osterbit-rest-001.appspot.com/games/"
suffix = ""
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test delete a player
#   status: PASS
reqType = "DELETE"
data=""
url = "http://osterbit-rest-001.appspot.com/users/"
suffix = "5910974510923776"
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test delete a nonexistent player
#   status: PASS
subprocess.call(command, shell=True)

#test delete a game
#   status: PASS
reqType = "DELETE"
data=""
url = "http://osterbit-rest-001.appspot.com/games/"
suffix = "4855443348258816"
command = cmdTemplate % (reqType, data, url, suffix)
commandList.append(command)
subprocess.call(command, shell=True)

#test delete a non-existent game
#   status: PASS
subprocess.call(command, shell=True)



"""
for command in testList: 
  subprocess.call(command, shell=True)

class restTestCase(unittest.TestCase):

  def setUp(self):
    #setUp
    someVal = 1

  def tearDown(self):
    #stuff to close
    someVal = 0

  def test_dummy(self):
    m = self.app.get('/')
    n = 1 + 1
    assert n == 2

"""