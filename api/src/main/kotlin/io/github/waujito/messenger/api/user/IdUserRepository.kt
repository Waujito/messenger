package io.github.waujito.messenger.api.user

class IdUserRepository : UserRepository {
    override fun getUserFromId(id: String): User {
        return User(id)
    }
}