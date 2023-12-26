package io.github.waujito.messenger.api.user

import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Repository

@Repository
class IdUserRepository(
        @Value("\${AS_USERINFO_URI}")
        private val userinfoUri: String
) : UserRepository {
    override fun getUserFromToken(token: String): User {
        val asUser = fetchAuthenticationServerUser(token, userinfoUri)

        return User(asUser.sub)
    }
}