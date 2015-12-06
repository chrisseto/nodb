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
Insert entries to a collection by calling ` db[collection_name].insert({'field': 'value'}) ` or to replace an entry, 
` db['col'][index] = {'new_fields' : 'new_values'} `. Note: To simply update an entry rather than replacing it entirely, use ` .update() `. Nothing enforces a flat entry, which allows for a field to have as its value a dictionary. However, nested fields will make querying slighly more difficult.
### Finding Data:
To find entries, use ` .filter() or .find() `. Both methods take in a ` Q ` object, several ` Q ` objects
 combined using ` & ` (AND) and ` | ` (OR), or a lambda function that returns ` True ` if the entry is to be returned. 
 Both methods return a collection instance, which can be read by coercing it to a list, or passed to any other method via chaining.
### Q:
 ` Q `s, or query objects, are used to create complicated queries simply. They have the format ` Q('field', 'operation', 'value') `.  Operations are ` eq ` for ` == `, ` ne ` for ` != `, ` in ` for ` in `, and ` ni `, for ` not in `.
 They can be combined in this manner: ` (Q() | Q()) & Q() `.
### Chaining:
 Since most methods return collections referring back to the original db, they can be chained to achieve more complicated functionality. 
 For example, to update all songs by Run the Jewels to contain genre:

 ` db['songs'].filter(Q('artist', 'eq', 'Run the Jewels')).update({'genre': 'rap'}) `

