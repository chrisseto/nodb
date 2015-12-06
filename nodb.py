import json


class Nodb():
    """
    file interactions need to be rewritten, currently file store is not working properly
    """
    def __init__(self, file_=False):
        if not file_:
            self.collections = {}
            return
        self.file_ = file_
        try:
            collections = json.load(self.file_)
        except (ValueError, IOError):
            print('Overriding File')
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

    def _write(self, file_=None):
        json.dump(self.read(), file_ or self.file_)

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

    def  __repr__(self):
        return '<Collection instance with name {0} and {1} items>'.format(self.name, len(list(self)))

    def insert(self, data):
        self.collection.append(data)
        return self.collection[-1]

    def replace(self, data, predicate=None):
        if predicate:
            collection = self.filter(predicate)
            for i in range(len(list(collection))):
                collection[i] = data
            return collection
        else:
            for i in range(len(list(self))):
                self.collection[i] = data
            return self.collection

    def update(self, data, predicate=None):
        if predicate:
            collection = self.filter(predicate)
            for i in range(len(list(self))):
                self.collection[i].update(data)
        else:
            for doc in self.collection:
                doc.update(data)

    def remove(self, predicate):
        doc = self.find_one(predicate)
        self.collection.remove(doc)

    def find(self, predicate):
        return self.filter(predicate)

    def filter(self, predicate):
        return self.__class__(self.name, filter(predicate, self.collection))

    def find_one(self, predicate):
        result = self.filter(predicate)
        if len(list(result)) != 1:
            raise Exception
        return result[0]

    def every(self, predicate):
        results = list(self.filter(predicate))
        return len(results) == len(self.collection)

    def difference(self, values):
        diffs = []
        for i in list(self):
            if i not in values:
                diffs.append(i)
        return self.__class__(self.name, diffs)

    #Index Methods! These are mostly useful for when order and/or index of items in the collection matter
    def at(self, indexes):
        return [self.collection[i] for i in indexes]

    def chunk(self, size=1):
        chunks = []
        l = len(list(self))
        r = l / size
        if r:
            for i in range(r - 1):
                chunks.append(self.__class__(self.name, self[(i * size):(i * size + size)]))
        if l % size:
            chunks.append(self.__class__(self.name, self[(l - size):l - 1]))
        return chunks

    def drop(self, n=1):
        return self.__class__(self.name, list(self)[n:]) if (n < len(list(self))) else self.__class__(self.name, [])

    def drop_right(self, n=1):
        return self.__class__(self.name, list(self)[0:(len(list(self)) - n)]) if (
            n < len(list(self))) else self.__class__(self.name, [])

    def drop_right_while(self, predicate):
        l = len(list(self)) - 1
        for i in range(l):
            if not predicate(self[l - i]):
                rest = l - i
                break
        return self.__class__(self.name, list(self)[:rest])

    def drop_while(self, predicate):
        l = len(list(self)) - 1
        for i in range(l):
            if not predicate(self[i]):
                rest = i
                break
        return self.__class__(self.name, list(self)[rest:])

    def sort(self, field, ascending=True):
        sortee = self.__class__(self.name, sorted(self.collection, key=lambda x: x[field]))
        return sortee if ascending else sortee.invert()

    def invert(self):
        l = len(self.collection) - 1
        inv = []
        for i in range(l):
            inv.append(self[l - i])
        inv.append(self[0])
        return self.__class__(self.name, inv)

    def rest(self):
        return self.__class__(self.name, self[1:])


# Query objects!
# Used in as predicate argument, as in db['collection'].find( Q('field', 'eq', 'value) )
# Can be combined for complex queries with AND (&) and OR (|), as in Q('field', 'eq', 'value) & Q('other_field', 'eq', 'value')
class Q():
    def __init__(self, field, op, val):
        self.field = field
        self.op = op
        self.val = val

    def __or__(self, other):
        return QQ(self, 'or', other)

    def __and__(self, other):
        return QQ(self, 'and', other)

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
        self.q1 = q1
        self.q2 = q2
        self.op = op

    def __call__(self, each):
        if self.op == 'and':
            return self.q1(each) and self.q2(each)
        else:
            return self.q1(each) or self.q2(each)
