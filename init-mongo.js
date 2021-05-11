db = db.getSiblingDB('social_networks')

db.createUser(
    {
        user: 'hub',
        pwd: 't6MbQtUL',
        roles: [
            {
                role: 'readWrite',
                db: 'social_networks'
            }
        ]
    }
);

db.createUser(
    {
        user: 'analyzer',
        pwd: 'pqq2BhwJ',
        roles: [
            {
                role: 'read',
                db: 'social_networks'
            }
        ]
    }
);
// Test the database

var error = false

var res = [
    db.container.createIndex({ myfield: 1 }, { unique: true }),
    db.container.createIndex({ thatfield: 1 }),
    db.container.insert({ myfield: 'hello', thatfield: 'testing' }),
    db.container.insert({ myfield: 'hello2', thatfield: 'testing' }),
    db.container.insert({ myfield: 'hello3', thatfield: 'testing' }),
    db.container.insert({ myfield: 'hello4', thatfield: 'testing' }),
    db.container.drop()
]

printjson(res)

if (error) {
    print('Error on creation, exiting (!)')
    quit(1)
} else {
    print('The database \'social_networks\' was successfully created')
}

db = db.getSiblingDB('intelligence')

db.createUser(
    {
        user: 'analyzer',
        pwd: 'RgK6Bnya',
        roles: [
            {
                role: 'readWrite',
                db: 'intelligence'
            }
        ]
    }
);

// Test the database

var error = false

var res = [
    db.container.createIndex({ myfield: 1 }, { unique: true }),
    db.container.createIndex({ thatfield: 1 }),
    db.container.insert({ myfield: 'hello', thatfield: 'testing' }),
    db.container.insert({ myfield: 'hello2', thatfield: 'testing' }),
    db.container.insert({ myfield: 'hello3', thatfield: 'testing' }),
    db.container.insert({ myfield: 'hello4', thatfield: 'testing' }),
    db.container.drop()
]

printjson(res)

if (error) {
    print('Error on creation, exiting (!)')
    quit(1)
} else {
    print('The database \'intelligence\' was successfully created')
}
//remove volume before building again