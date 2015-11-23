import json

class NoDb():

	def __init__(self, file_=False):
		if not file_:
			self.collections = {}
			return
		self.file_ = file_
		try:
			collections = json.load(self.file_)
		except (ValueError, IOError):
			print 'Overriding File'
			json.dump({}, self.file_)
			collections = json.load(self.file_)            

		for key, val in collections.iteritems():
			self.collections[key] = Collection(key, val)

	def __getitem__(self, col):
		collection = self.collections.get(col)
		if not collection:
			collection = Collection(col)
			self.collections[col] = collection
		return collection
    
	def _write(self):
		json.dump(self.read(), self.file_)

	def read(self):
		noDb = {}
		for key, collection in self.collections.iteritems():
			noDb[key] = collection.read()
		return noDb

	def save(self):
		self._write()

	
class Collection():

	def __init__(self, name, data=None):
		self.name = name
		self.collection = data or []

	def _filter(self, query, doc, nested=True):
		for key, val in query.iteritems():
			if type(doc.get(key)) == (tuple or list) and type(val) != (tuple or list) and nested:
				if val not in doc.get(key):
					return False
			elif type(doc.get(key)) == (tuple or list) and type(val) == tuple or list and nested:
				for v in val:
					if v not in doc.get(key):
						return False
			elif type(doc.get(key)) == dict and type(val) == dict and nested:
				if not self._filter(query=val, doc=doc.get(key)):
					return False
			elif doc.get(key) != val:
				return False
		return True

	def insert(self, data):
		self.collection.append(data)
		return self.collection[-1]

	def replace(self, query, data):
		index = self.find_one(query, index=True)
		self.collection[index] = data
		return self.collection[index]

	def update(self, query, data):
		indexes = self.find(query, index=True)
		for index in indexes:
			self.collection[index].update(data)

	def remove(self, query):
		doc = self.find_one(query)
		self.collection.remove(doc)

	def find(self, query, index=False):
		for ind, doc in enumerate(self.collection):
			if self._filter(query, doc):
				yield ind if index else doc

	def find_one(self, query, index=False):
		results = list(self.find(query, index))
		if len(results) != 1:
			raise Exception
		return results[0]

	def read(self):
		return self.collection
