import json
import itertools

class Nodb():

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

	def load(self, data):
		for key, val in data.iteritems():
			self.collections[key] = Collection(key, val)

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

	def __getitem__(self, index):
		return self.collection[index]

	def __iter__(self):
		return iter(self.collection)

	def insert(self, data):
		self.collection.append(data)
		return self.collection[-1]

	def replace(self, query, data):
		index = self.find_one(query, index=True)
		self.collection[index] = data
		return self.collection[index]

	def update(self, data, query=None):
		if query:
			indexes = self.find(query, index=True)
			for index in indexes:
				self.collection[index].update(data)
		else:
			for doc in self.collection:
				doc.update(data)

	def remove(self, query):
		doc = self.find_one(query)
		self.collection.remove(doc)

	def find(self, query, index=False):
		for ind, doc in enumerate(self.collection):
			if self._filter(query, doc):
				yield ind if index else doc

	def filter(self, predicate):
		return self.__class__(self.name, filter(predicate, self.collection))

	def find_one(self, query, index=False):
		results = list(self.find(query, index))
		if len(results) != 1:
			raise Exception
		return results[0]

	def every(self, query):
		results = list(self.find(query))
		return len(results) == len(self.collection)

	def at(self, indexes):
		return [self.collection[i] for i in indexes]

	def countBy(self, *args, **kwargs):
		raise NotImplementedError


class Q():
	def __or__(self, other):
		return QQ(self, 'or', other)

	def __and__(self, other):
		return QQ(self, 'and', other)

	def __init__(self, field, op, val):
		self.field = field
		self.op = op
		self.val = val

	def __call__(self, each):
		if self.op == 'in':
			return self.val in each[self.field]
		elif self.op == 'ni':
			return self.val not in each[self.field]
		elif self.op == 'eq':
			return self.val == each[self.field]
		elif self.op == 'ne':
			return self.val != each[self.field]
		else:
			raise BaseException

class QQ(Q):
	def __init__(self, q1, op, q2):
		if not isinstance(q1, QQ):
			self.qs = [q1, op, q2]
		else:
			qs = [q1.qs, op, q2]
			self.qs = list(itertools.chain(*qs)
		'''
		self.op = op
		self.qs = []
		for q in args:
			if isinstance(q, QQ) and q.op == op:
				self.qs += q.qs
			else:
				self.qs.append(q)
		'''
	def __call__(self, each):
		return reduce(lambda left, op, rigth: left(each) and right(each) if op == 'and' else left(each) or right(each), self.qs)

