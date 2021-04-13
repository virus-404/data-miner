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

// Test the database

let error = false

let res = [
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
//remove volume before building again 