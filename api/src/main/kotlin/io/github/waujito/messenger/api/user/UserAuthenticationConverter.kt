package io.github.waujito.messenger.api.user

import org.springframework.core.convert.converter.Converter
import org.springframework.security.authentication.AbstractAuthenticationToken
import org.springframework.security.core.authority.SimpleGrantedAuthority
import org.springframework.security.oauth2.jwt.Jwt
import org.springframework.security.oauth2.server.resource.authentication.JwtGrantedAuthoritiesConverter

/**
 * Converts JWT token to the User Authentication
 */
class UserAuthenticationConverter(
        private val userRepository: UserRepository
) :
        Converter<Jwt, AbstractAuthenticationToken> {
    override fun convert(jwt: Jwt): AbstractAuthenticationToken {
        val token = jwt.tokenValue
        val user = userRepository.getUserFromToken(token)

        val grantedAuthoritiesConverter = JwtGrantedAuthoritiesConverter()

        val authorities = grantedAuthoritiesConverter.convert(jwt)?.toMutableList() ?: mutableListOf()
        authorities.add(SimpleGrantedAuthority("SCOPE_user"))


        val authentication = UserAuthenticationToken(user, authorities)
        authentication.isAuthenticated = true

        return authentication
    }
}