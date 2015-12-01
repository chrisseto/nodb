import pytest

from nodb import *


@pytest.fixture
def populate_data():
    return {
        'people': [
            {'name': 'Chance',
             'profession': 'musician',
             'age': 22},
            {'name': 'Donnie Trumpet',
             'profession': 'musician',
             'age': False},
            {'name': 'Peter',
             'profession': 'producer',
             'age': False
             }
        ],
        'songs': [
            {'title': 'Miracle',
             'by': 'Donnie Trumpet'},
            {'title': 'Home Studio',
             'by': 'Chance'},
        ],
    }

@pytest.fixture
def collection_data():
    return [
        {'name':'Everything I Saw',
         'number': 1,
         'type':'song'},
        {'name':'Came so Easy',
         'number': 2,
         'type':'song'},
        {'name':'Trying',
         'number': 3,
         'type':'song'},
        {'name':'Traveller',
         'number': 4,
         'type':'song'},
        {'name':'Chip on my Shoulder',
         'number': 5,
         'type':'song'}
    ]

def test_filter(populate_data):
    db = Nodb()
    db.load(populate_data)
    miracles = db['songs'].filter(lambda x: x['title'] == 'Miracle')
    assert len(list(miracles)) == 1


def test_find_one(populate_data):
    db = Nodb()
    db.load(populate_data)
    assert db['people'].find_one(Q('name', 'eq', 'Chance'))


def test_update(populate_data):
    db = Nodb()
    db.load(populate_data)
    db['people'].update({'profession': 'rapper'}, {'name': 'Chance'})
    assert db['people'].find_one(Q('name', 'eq', 'Chance'))['profession'] == 'rapper'


def test_chain(populate_data):
    db = Nodb()
    db.load(populate_data)
    db['people'].filter(lambda x: x['age'] == 22).update({'profession': 'rapper'})
    assert db['people'].find_one(Q('name', 'eq', 'Chance'))['profession'] == 'rapper'


def test_Q(populate_data):
    db = Nodb()
    db.load(populate_data)
    chance = db['people'].filter(
        Q('name', 'eq', 'Chance')
    )
    assert len(list(chance)) == 1
    assert list(chance)[0]['name'] == 'Chance'


def test_Q_and(populate_data):
    db = Nodb()
    db.load(populate_data)
    chance = db['people'].filter(
        Q('profession', 'eq', 'musician') & Q('age', 'eq', 22)
    )
    assert len(list(chance)) == 1
    assert list(chance)[0]['name'] == 'Chance'


def test_Q_or(populate_data):
    db = Nodb()
    db.load(populate_data)
    sox = db['people'].filter(
        Q('name', 'eq', 'Donnie Trumpet') | Q('name', 'eq', 'Chance')
    )
    assert len(list(sox)) == 2


def test_Q_big(populate_data):
    db = Nodb()
    db.load(populate_data)
    sox = db['people'].filter(
        Q('name', 'eq', 'Donnie Trumpet') | Q('name', 'eq', 'Chance') | Q('profession', 'eq', 'producer')
    )
    assert len(list(sox)) == 3


def test_Q_big_and(populate_data):
    db = Nodb()
    db.load(populate_data)
    sox = db['people'].filter(
        ((Q('name', 'eq', 'Donnie Trumpet') | Q('name', 'eq', 'Chance')) & Q('profession', 'eq', 'producer'))
    )
    assert len(list(sox)) == 0


def test_Q_big_and_true(populate_data):
    db = Nodb()
    db.load(populate_data)
    sox = db['people'].filter(
        Q('name', 'eq', 'Donnie Trumpet') | Q('name', 'eq', 'Chance') & Q('profession', 'eq', 'musician')
    )
    assert len(list(sox)) == 2


def test_Q_and_simple():
    qq = Q('id', 'eq', 2) | Q('id', 'eq', 1)
    assert qq({'id': 1}) is True
    assert qq({'id': 2}) is True
    assert qq({'id': 3}) is False


def test_Q_and_complex():
    qq = (Q('id', 'eq', 2) | Q('id', 'eq', 1)) & Q('type', 'eq', 'foo')
    assert qq({'id': 1, 'type': 'foo'}) is True
    assert qq({'id': 2, 'type': 'foo'}) is True
    assert qq({'id': 3, 'type': 'foo'}) is False

    assert qq({'id': 1, 'type': 'bar'}) is False

def test_every(collection_data):
    c = Collection('All of it Was Mine', collection_data)
    assert c.every(lambda x: x['type'] == 'song')

def test_difference(collection_data):
    c = Collection('All of it Was Mine', collection_data)
    values = [{'name': 'Everything I Saw', 'number': 1, 'type':'song'},
        {'name' :'Came so Easy', 'number': 2, 'type':'song'}]
    r = c.difference(values)
    assert list(r) == [{'name': 'Trying','number': 3,'type':'song'},
        {'name':'Traveller', 'number': 4, 'type':'song'},
        {'name':'Chip on my Shoulder', 'number': 5, 'type':'song'}]
