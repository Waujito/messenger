package io.github.waujito.messenger.api.user

/**
 * Defines the methods that may be used to retrieve the user
 */
interface UserRepository {
    fun getUserFromId(id: String): User
}