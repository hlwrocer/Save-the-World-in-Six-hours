from flask_pymongo import PyMongo
import datetime

'''
_Accounts_
{
username 
password 
uid
}

_acc_info_
uid
address
phone #
contacts [
	uid1, 
	uid2, 
	uid3
]
updateFreq: int (min 1 - max 3)

_-uid-_input_
date
mood
appetite
productivity
sleep
energy

'''

class stwishDB():
	mongo = object

	def __init__(self, app):
		global mongo
		mongo = PyMongo(app)

	# Assumes userDict contains {uid, username, password}
	def createAccount(self, userDict):
		last = mongo.db['accounts'].find(limit=1, sort=[('uid', -1)])
		print(last.count())
		if last.count() > 0:
			userDict['uid'] = last[0]['uid']+1
		else:
			userDict['uid'] = 1000000
		
		if self.getUID(userDict) == None:
			result = mongo.db['accounts'].insert_one(userDict)
			return {'uid':userDict['uid']}	#returns acknowledged(a boolean) and inserted_id
		else:
			return None

	def getAccount(self, uidDict):
		return mongo.db['accounts'].find_one(uidDict)


	def getUID(self, usernameDict):
		account = mongo.db['accounts'].find_one(usernameDict)
		if account:
			return {'uid':account['uid']}
		else:
			return None

	def createAccInfo(self, infoDict):
		# if infoDict['updateFreq'] > 3:
		# 	infoDict['updateFreq'] = 3
		# elif infoDict['updateFreq'] < 1:
		# 	infoDict['updateFreq'] = 1

		result = mongo.db['acc_info'].insert_one(infoDict)
		if result.acknowledged:
			return {'uid':result.inserted_id}
		else:
			return None

	def getAccInfo(self, uidDict):
		return mongo.db['acc_info'].find_one(uidDict)

			#untested
	def editAccount(self, updatedDict):
		updated = mongo.db['accounts'].find_one_and_update({'uid':updatedDict['uid']}, updatedDict)
		for key in updatedDict:
			if updatedDict[key] != updated[key]:
				return None
		return updated
			#untested
	def editAccInfo(self, updatedDict):
		updated = mongo.db['acc_info'].find_one_and_update({'uid':updatedDict['uid']}, updatedDict)
		for key in updatedDict:
			if updatedDict[key] != updated[key]:
				return None
		return updated

	def addInput(self, inputDict):
		collName = str(inputDict['uid']) + "_input"
		today = datetime.date.today();
		inputDict['date'] = today.strftime("%Y%m%d")
		result = mongo.db[collName].insert_one(inputDict)
		if result.acknowledged:
			return {'uid':result.inserted_id}
		else:
			return None

	def getInput(self, uidDict, n):
		collName = str(uidDict['uid']) + "_input"
		result = mongo.db[collName].find(uidDict, limit=n, sort=[('date', -1), ('id', -1)])
		return result

	def getFrequency(self, uidDict):
		return self.getAccInfo(uidDict)['updateFreq']

	def getContacts(self, uidDict):
		return self.getAccInfo(uidDict)['contacts']
