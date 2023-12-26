package io.github.waujito.messenger.api.user

import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import org.springframework.security.core.AuthenticationException
import org.springframework.security.web.AuthenticationEntryPoint

/**
 * Returns an error if the authentication failed
 */
class UserAuthenticationEntryPoint : AuthenticationEntryPoint {
    override fun commence(
            request: HttpServletRequest,
            response: HttpServletResponse,
            authException: AuthenticationException
    ) {
        response.status = 401
        response.addHeader("WWW-Authenticate", "Bearer")
        response.contentType = "application/json"
        response.outputStream.print(
                "{\"error\": \"Authentication error\", " +
                        "\"message\": \"${authException.message}\""
        )
        response.outputStream.flush()
    }
}