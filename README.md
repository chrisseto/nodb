# NODB!

Nodb is a simple database replacement for prototyping, testing, hackathons, and whatever else. It features memory-only and save to file capabilities, an awesome composable query syntax, and many convinient methods. It borrows heavily from lodash and lowdb.

## Starting Out!
### Creating (or loading) a db:
` db = Nodb() ` or ` db = Nodb('filename.json') `,
### Saving it:
` db.save() ` or ` db.save('filename.json') ` 
### Accessing Data:
A Nodb instance is organized in collections, which can be accessed through ` db['collection_name'] `.
To read from a collection, simply coerce the collection to a list (` list(db['col']) `), directly iterate, or call by index.
` for val in db['col']: ` or ` db['col'][0] `
### Inputting Data:
Insert entries to a collection by calling ` db[collection_name].insert({'field': 'value'}) `

