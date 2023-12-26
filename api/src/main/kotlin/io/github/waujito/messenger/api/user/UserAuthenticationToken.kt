package io.github.waujito.messenger.api.user

import org.springframework.security.authentication.AbstractAuthenticationToken
import org.springframework.security.core.GrantedAuthority

/**
 * A user Authentication
 */
class UserAuthenticationToken(
        private val user: User,
        authorities: Collection<GrantedAuthority>?,
) : AbstractAuthenticationToken(authorities) {
    override fun getCredentials() = null
    override fun getPrincipal() = user
}