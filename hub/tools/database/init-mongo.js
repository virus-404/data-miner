db.createUser(
    {
        user: "hub",
        password: "t6MbQtUL",
        roles: [
            {
                role: "readWrite",
                db: "data"
            }
        ]
    }
)
//https://medium.com/faun/managing-mongodb-on-docker-with-docker-compose-26bf8a0bbae3